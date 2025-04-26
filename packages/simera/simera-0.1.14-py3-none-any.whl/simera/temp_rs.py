import os
from datetime import date, datetime, timedelta
from time import perf_counter
from glob import glob
from itertools import product, chain
from string import digits, ascii_uppercase
from blachnio.ds import read_excel
import ast
import hashlib
import pickle
import math
from tqdm import tqdm
import pandas as pd
import numpy as np
from warnings import warn
from app.paths import PATH_DIR_TRANSPORT_RATES_DOWNSTREAM, PATH_FILE_MASTER_MAPPER
from app.utils import expand_df_with_list_input
tqdm.pandas()


class ShipmentCostDetails:
    def __init__(self, shipment_id, ratesheet_id, ratesheet_desc):
        """It's used to store shipment level cost data in Shipment class object """
        self.shipment_id = shipment_id
        self.ratesheet_id = ratesheet_id
        self.ratesheet_desc = ratesheet_desc
        self.parts_of_shipments = []
        self.parts_cost_details = []
        self.parts_cost_used = []
        self.parts_cost_summary = []
        # Summaries

    def add_shipment_cost_data(self, shipment_parts, df_cost_details, df_cost_used, df_cost_summary):
        self.parts_of_shipments.append(shipment_parts)
        self.parts_cost_details.append(df_cost_details)
        self.parts_cost_used.append(df_cost_used)
        self.parts_cost_summary.append(df_cost_summary)

    @property
    def df_cost_summary_details(self):
        """Calculate cost summary by adding summary parts and multiplying results by cost units"""
        return pd.concat(self.parts_cost_summary).reset_index(drop=True)

    @property
    def df_cost_summary(self):
        """Return single row cost summary for all shipment part"""
        cost_columns = [col for col in self.df_cost_summary_details.columns if col.startswith('cost_')]
        outcome = self.df_cost_summary_details[cost_columns].mul(self.df_cost_summary_details['units'], axis=0).sum().to_frame().T
        # Add fuel surcharge
        outcome.insert(outcome.columns.get_loc('cost_fuel_surcharge'), 'fuel_surcharge-%', self.df_cost_summary_details['fuel_surcharge-%'].unique())
        outcome['units_total'] = self.df_cost_summary_details['units'].sum()
        outcome['units_max-size'] = self.df_cost_summary_details[self.df_cost_summary_details['part'].str.startswith('max-size')]['units'].fillna(0).sum()
        outcome['parts'] = self.df_cost_summary_details['part'].sum()
        return outcome

    def __str__(self):
        return f'Shipment {self.shipment_id} Ratesheet {self.ratesheet_id} {self.ratesheet_desc} Parts {self.df_cost_summary.units_total.sum()}'


class ShipmentCost:
    CURRENT_PROCESSING_TIME_SHIPMENTS_PER_SECOND = 41.6
    UOM_WEIGHT_CHARGEABLE_INCREASED = ['kg', 'lbs']
    UOM_VOLUME_CHARGEABLE_INCREASED = ['m3', 'cft']
    COST_TYPES_BEHAVIOUR = {'min': 'top', 'fix': 'sum', 'var': 'sum', 'fsc': 'top', 'lhl': 'sum', 'ext': 'sum'}

    def __init__(self, shipment_input, ratesheet_input):
        """
        Shipment calculates cost based on data input and TransportRateSheet content.

        :param shipment_input: [dict | list of dicts | pd.DataFrame].
        Shipment input data. Note: make sure to maintain proper dtypes when reading excel table.
            String-type values are treated as 'dimensions': Accepted items:
                data={'dest_ctry': 'PL', 'dest_zip': '12345', src: 'DC_PL_X'}
            Numeric values will be treated as 'measures' and accept any cost UOM used in ratesheet.
                data={'m3': 2.3, 'kg': 340, 'pal': 1.2}
        :param ratesheet_input: [TransportRateSheet | list of TransportRateSheet].
        Ratesheet input with all needed data to calculate cost.
        """
        self.time_start = perf_counter()
        self.shipments = []

        self.shipment_input = self._get_shipment_input_data(shipment_input)
        self.ratesheet_input = self._get_ratesheet_input_data(ratesheet_input)
        self.shipment_input_measures_columns = self._get_shipment_columns_with_measures()
        self.shipment_input_dimensions_columns = self._get_shipment_columns_with_dimensions()

        # Get and limit set of ratesheets used in calculation based on destination country
        self.ratesheet_scope, self.shipments_allocated_to_ratesheets = self._get_ratesheets_in_scope_and_expanded_shipments_dataset()
        self.shipments_df_initial = self._get_shipment_df_extended_with_ratesheets()
        self.shipments_df_dimensions = self.shipments_df_initial[self.shipment_input_dimensions_columns]
        self.shipments_df_measures_1_initial = self.shipments_df_initial[self.shipment_input_measures_columns]
        self.shipments_df_measures_2_calculated = self.shipments_df_measures_1_initial.copy()
        self.shipments_df_core = self.shipments_df_initial[['shipment_id', 'ratesheet_id']].copy()
        self.shipments_df_debug = self.shipments_df_core.copy()

        # Get zone and LT available in ratesheets
        self._get_shipment_attribute_zone_and_leadtime()

        # Get all required measures for shipments (based on ratesheet)
        # This fills table: self.shipments_df_measures_2_calculated
        self._get_shipment_attribute_required_measures()

        # Get chargeable ratios
        # This fills table: self.shipments_df_measures_3_chargeable
        self.shipments_df_measures_3_chargeable = pd.DataFrame(self.shipments_df_measures_2_calculated.copy(), dtype=float)
        self._get_shipment_attribute_chargeable_measures()

        # Get shipments details and store it in self.shipments
        self.shipments_df_cost = pd.DataFrame(index=self.shipments_df_core.index, columns=None, dtype=float)
        # This fills table: self.shipments_df_cost
        self._get_shipment_attribute_cost()

        # Make summary tables
        # note turn them on again
        self.shipments_output_details = self._get_shipment_output()
        self.shipments_output_best_cost, self.shipments_output_best_missing = self._get_shipment_output_best()

    @staticmethod
    def _get_shipment_input_data(shipment_input):
        """Converts shipment_input data into pd.DataFrame with proper dtypes"""
        if isinstance(shipment_input, dict):
            df = pd.DataFrame(shipment_input, index=[0])
        elif isinstance(shipment_input, (list, tuple)):
            df = pd.DataFrame(shipment_input, index=range(len(shipment_input)))
        elif isinstance(shipment_input, pd.DataFrame):
            df = pd.DataFrame(shipment_input)
        else:
            raise TypeError(f'Shipment does not have proper shipment_data type. Received value: {type(shipment_input)}'
                            '\nAccepted types: [dict, list, pd.DataFrame]')
        df['shipment_id'] = df.index
        return df

    def _get_shipment_columns_with_measures(self):
        """Returns list of initial shipment input measures"""
        exclude_columns = ['shipment_id']
        filter_columns = [col for col in self.shipment_input if col.startswith('filter_')]
        exclude_columns.extend(filter_columns)
        measures = [col for col in self.shipment_input.select_dtypes('number').columns if col not in exclude_columns]
        return measures

    def _get_shipment_columns_with_dimensions(self):
        """Returns list of initial shipment input dimensions"""
        exclude_columns = ['shipment_id']
        exclude_columns.extend(self.shipment_input_measures_columns)
        dimensions = [col for col in self.shipment_input.columns if col not in exclude_columns]
        return dimensions

    @staticmethod
    def _get_ratesheet_input_data(ratesheet_input):
        """Return list of ratesheets to be used for shipment processing"""
        verified_ratesheets = []
        if isinstance(ratesheet_input, (list, tuple)):
            return ratesheet_input
        else:
            verified_ratesheets.append(ratesheet_input)
            return verified_ratesheets

    def _get_ratesheets_in_scope_and_expanded_shipments_dataset(self):
        """Return subset of ratesheets with countries in shipment_input scope and expanded shipments_df"""

        # For each ratesheet find shipments in scope (shipment dest_ctry exists in ratesheet dest_ctry)
        shipment_ids_per_ratesheets = {}
        for ratesheet in self.ratesheet_input:
            mask_ctry = self.shipment_input.dest_ctry.isin(ratesheet.ratesheet_countries)
            mask_scope = mask_ctry
            if shipments_ids := self.shipment_input.loc[mask_scope]['shipment_id'].unique().tolist():
                shipment_ids_per_ratesheets.update({ratesheet.meta_ratesheet_id: shipments_ids})

        ratesheets_in_scope = [rs for rs in self.ratesheet_input if rs.meta_ratesheet_id in shipment_ids_per_ratesheets]
        # Convert dict shipment_ids_per_ratesheets into DataFrame
        # wise - potential candidate for performance check
        keys = chain.from_iterable([[k] * len(v) for k, v in shipment_ids_per_ratesheets.items()])
        values = chain.from_iterable(shipment_ids_per_ratesheets.values())
        shipments_df = pd.DataFrame({'ratesheet_id': keys, 'shipment_id': values})
        print(f'Ratesheets in scope for shipment_input: {len(ratesheets_in_scope)}/{len(self.ratesheet_input)}')
        return ratesheets_in_scope, shipments_df

    def _get_shipment_df_extended_with_ratesheets(self):
        """Extends (merge) initial shipment_input with ratesheet"""
        df = self.shipment_input.merge(self.shipments_allocated_to_ratesheets, how='left', on='shipment_id')
        print(f'Ratesheet-shipment combinations: {df.shape[0]}.'
              f'\nEstimated processing time: {df.shape[0] / self.CURRENT_PROCESSING_TIME_SHIPMENTS_PER_SECOND :0,.1f} sec. Shound be finished by '
              f'{(datetime.now() + timedelta(seconds=(df.shape[0] / self.CURRENT_PROCESSING_TIME_SHIPMENTS_PER_SECOND))).strftime('%H:%M:%S')}'
              f'(now is {datetime.now().strftime('%H:%M:%S')})')
        return df

    def _get_shipment_attribute_zone_and_leadtime(self):
        """Returns (if exists) shipment zone and leadtimes from ratesheet."""

        # Get DataFrame of shipments for given ratesheet
        # print('Step 1/4. Finding zone and leadtime:')
        for ratesheet in tqdm(self.ratesheet_scope, desc='Step 1/4. Finding zone and leadtime'.ljust(45, '.'), unit='ratesheet'):
            shipments_sub_df = self.shipments_df_dimensions[self.shipments_df_core.ratesheet_id == ratesheet.meta_ratesheet_id]

            # For each shipment in shipments_sub_df we need to find zone and lead-time
            for shipment_idx, shipment_row in shipments_sub_df.iterrows():
                initial_dimensions = shipment_row[shipment_row.notna()].to_dict()
                self.shipments_df_debug.loc[shipment_idx, 'initial_dimensions'] = str(initial_dimensions)

                # Zone lookup
                mask_ctry = (shipment_row.dest_ctry == ratesheet.zone_df_zone.zone_ctry)
                mask_zip = (shipment_row.dest_zip >= ratesheet.zone_df_zone.zip_from) & (shipment_row.dest_zip <= ratesheet.zone_df_zone.zip_to)
                ratesheet_zones_found_df = ratesheet.zone_df_zone[mask_ctry & mask_zip]

                zones_found = ratesheet_zones_found_df['zone_id'].unique()
                # Raise error if more then one zone found:
                if len(zones_found) > 1:
                    print(ratesheet_zones_found_df)
                    raise DataInputError(message='Too many zones found. Only 1 allowed. Correct inputs.', io=ratesheet.source_io,
                                         worksheet=ratesheet.source_worksheet, column='zone_ctry|zone_zip|zone_id',
                                         values=f'Zones found: {zones_found}')
                if zones_found.size > 0:
                    zone = zones_found[0]
                    zone_zip_range = f'{ratesheet_zones_found_df.zip_from.values[0]}-{ratesheet_zones_found_df.zip_to.values[0]}'

                    self.shipments_df_core.loc[shipment_idx, 'zone'] = zone
                    self.shipments_df_debug.loc[shipment_idx, ['zone', 'zone_zip_range']] = (zone, zone_zip_range)

                # Lead-time lookup
                mask_ctry = (shipment_row.dest_ctry == ratesheet.zone_df_leadtime.zone_ctry)
                mask_zip = (shipment_row.dest_zip >= ratesheet.zone_df_leadtime.zip_from) & (shipment_row.dest_zip <= ratesheet.zone_df_leadtime.zip_to)
                ratesheet_leadtime_found_df = ratesheet.zone_df_leadtime[mask_ctry & mask_zip]
                leadtime_found = ratesheet_leadtime_found_df['zone_lt'].unique()



                # Raise error if more then one zone found:
                if len(leadtime_found) > 1:
                    print(ratesheet_leadtime_found_df)
                    raise DataInputError(message='Too many leadtimes found. Only 1 allowed. Correct inputs.', io=ratesheet.source_io,
                                         worksheet=ratesheet.source_worksheet, column='zone_ctry|zone_zip|zone_lt',
                                         values=f'Leadtimes found: {leadtime_found}')
                if leadtime_found.size > 0:
                    leadtime = leadtime_found[0]
                    leadtime_zip_range = f'{ratesheet_leadtime_found_df.zip_from.values[0]}-{ratesheet_leadtime_found_df.zip_to.values[0]}'

                    # Add zone info to shipment_sub_df
                    self.shipments_df_core.loc[shipment_idx, 'leadtime'] = leadtime
                    self.shipments_df_debug.loc[shipment_idx, ['leadtime', 'leadtime_zip_range']] = (leadtime, leadtime_zip_range)

        # Add empty columns if no output was returned
        for col in ['zone', 'zone_zip_range', 'leadtime', 'leadtime_zip_range']:
            if col not in self.shipments_df_debug.columns:
                self.shipments_df_debug[col] = np.nan
        for col in ['zone', 'leadtime']:
            if col not in self.shipments_df_core.columns:
                self.shipments_df_core[col] = np.nan

    def _get_shipment_attribute_required_measures(self):
        """Extends initial shipment measures to get all required uoms by a ratesheet"""

        # Get DataFrame of shipments for given ratesheet with zone.
        # print('\rSTep 2/4. Getting requested measures:')
        for ratesheet in tqdm(self.ratesheet_scope, desc='Step 2/4. Getting requested measures'.ljust(45, '.'), unit='ratesheet'):
            mask_ratesheet = (self.shipments_df_core.ratesheet_id == ratesheet.meta_ratesheet_id)
            mask_zone_exist = (self.shipments_df_core.zone.notna())
            shipments_sub_df = self.shipments_df_measures_1_initial[mask_ratesheet & mask_zone_exist]

            # For each shipment in shipments_sub_df we need to find measures (dict)
            for shipment_idx, shipment_row in shipments_sub_df.iterrows():
                # Measures_netto is a dict
                initial_measures = shipment_row[shipment_row.notna()].to_dict()

                if 'shipment' not in initial_measures:
                    initial_measures['shipment'] = 1
                self.shipments_df_debug.loc[shipment_idx, 'initial_measures'] = str(initial_measures)
                self.shipments_df_debug.loc[shipment_idx, 'required_measures'] = str(ratesheet.cost_uoms_required)

                # Check required uoms that are missing
                initial_measures_missing = []
                for uom in ratesheet.cost_uoms_required:
                    if uom not in initial_measures.keys():
                        initial_measures_missing.append(uom)

                # # Calculate required values that are missing
                df_cost = ratesheet.cost_df_uoms_ratios.copy()
                initial_measures_missing_source = {}
                if initial_measures_missing:
                    for uom in initial_measures_missing:
                        df_uom = df_cost[(df_cost.uom_to == uom) & df_cost.uom_from.isin(initial_measures.keys())].head(1).squeeze()
                        if df_uom.shape[0]:
                            initial_measures_missing_source[uom] = f'from {df_uom.uom_from} using {df_uom.ratio}={df_uom.value}'
                            initial_measures[uom] = round(initial_measures.get(df_uom.uom_from) / df_uom.value, 8)
                        else:
                            raise DataInputError(message=f'Impossible to calculate all required uoms for shipment to calculate cost.'
                                                         f'\n{" "*16}Shipment available uom: {initial_measures}'
                                                         f'\n{" "*16}Shipment missing uom: {initial_measures_missing}'
                                                         f'\n{" "*16}Solution A: Add more uoms to shipment values'
                                                         f'\n{" "*16}Solution B: Add more ratios to ratesheet meta_item to cover missing uoms'
                                                         f'\n{" "*16}Current content of ratio_cost_uom: {ratesheet.meta_ratio_cost_uom})',
                                                 io=ratesheet.source_io, worksheet=ratesheet.source_worksheet,
                                                 column='meta_item', values='ratio_cost_uom')

                # Add data to shipment_df
                for k, v in initial_measures.items():
                    self.shipments_df_measures_2_calculated.loc[shipment_idx, k] = v
                self.shipments_df_debug.loc[shipment_idx, 'measures_missing'] = str(initial_measures_missing)
                self.shipments_df_debug.loc[shipment_idx, 'measures_calculated'] = str(initial_measures_missing_source)

    def _get_shipment_attribute_chargeable_measures(self):
        """Applies chargeable ratio. Input must be given as dict: e.g. {'kg/m3': 167}
        Currently supported only input as kg/m3. For Parcel DIMS, recalculate to get this (cm*cm*cm/kg=ratio~5000)
        (the approach will evolve once I get more examples, for now only chargeable weight in parcel is used)
        Approach: Adjust volume or weight to reach chargeable ratio level.
        Example:
        chargeable='kg/m3'=167, shipment_values={'kg': 100, 'm3': 1} -> shipment_values_charge={'kg': 167, 'm3': 1}
        chargeable='kg/m3'=167, shipment_values={'kg': 200, 'm3': 1} -> shipment_values_charge={'kg': 200, 'm3': 1.19}
        """
        # print('\rStep 3/4. Getting chargeable measures:')
        for ratesheet in tqdm(self.ratesheet_scope, desc='Step 3/4. Getting chargeable measures'.ljust(45, '.'), unit='ratesheet'):
            mask_ratesheet = (self.shipments_df_core.ratesheet_id == ratesheet.meta_ratesheet_id)
            mask_zone_exist = (self.shipments_df_core.zone.notna())
            shipments_sub_df = self.shipments_df_measures_2_calculated[mask_ratesheet & mask_zone_exist]

            # For each shipment in shipments_sub_df we need to get chargeable measures (dict)
            for shipment_idx, shipment_row in shipments_sub_df.iterrows():
                values_chargeable = shipment_row[shipment_row.notna()].to_dict()
                chargeable_ratios = ratesheet.meta_ratio_cost_chargeable
                self.shipments_df_debug.loc[shipment_idx, 'chargeable_ratios'] = str(chargeable_ratios)
                self.shipments_df_debug.loc[shipment_idx, 'max_size'] = str(ratesheet.meta_max_shipment_size)
                if chargeable_ratios:
                    # Only one chargeable ratio is allowed now, but maybe it will be needed to have more, so I used loop.
                    for chargeable_uoms, chargeable_value in chargeable_ratios.items():
                        chargeable_uom_weight, chargeable_uom_volume = chargeable_uoms.split('/')
                        # Determine actual shipment_ratio and compare with chargeable_ratio
                        # Calculate what shipment weight should be vs initial values
                        shipment_weight = values_chargeable.get(chargeable_uom_weight)
                        shipment_volume = values_chargeable.get(chargeable_uom_volume)
                        # Calculate chargeable m3 and kg
                        shipment_weight_chargeable = max(shipment_volume * chargeable_value, shipment_weight)
                        shipment_volume_chargeable = max(shipment_weight * (1/chargeable_value), shipment_volume)
                        # Get ratios with which all weight and volume uoms will be increased
                        shipment_weight_increase = shipment_weight_chargeable / shipment_weight
                        shipment_volume_increase = shipment_volume_chargeable / shipment_volume
                        # Increase all volume or weight uoms with proper increase_ratio
                        for uom in self.UOM_WEIGHT_CHARGEABLE_INCREASED:
                            if uom in values_chargeable:
                                values_chargeable[uom] = round(values_chargeable[uom] * shipment_weight_increase, 8)
                        for uom in self.UOM_VOLUME_CHARGEABLE_INCREASED:
                            if uom in values_chargeable:
                                values_chargeable[uom] = round(values_chargeable[uom] * shipment_volume_increase, 8)

                        # Write outcome to new dataset
                        for k, v in values_chargeable.items():
                            self.shipments_df_measures_3_chargeable.loc[shipment_idx, k] = v

    @staticmethod
    def _split_shipment_into_parts_based_on_max_size(shipment_values, shipment_max_size):
        """Split the original shipment_values (dict) into max-size and remaining parts.
        Max-size units can be 0-N, Below-max can get 0 or 1.
        Example:
            shipment_values={'m3': 3, 'kg': 60} and shipment_max_size={'kg': 25}
        parts_max_size = {'m3': 1.25, 'kg': 25.0}
        parts_remaining = {'m3': 0.5, 'kg': 10.0}"""

        do_not_split_uoms = ['shipment']
        max_uom, max_val = next(iter(shipment_max_size.items()))  # Only first dict entry used; future extend if needed

        # Check how many max-size and remaining-size parts exist in shipment
        units_all = shipment_values[max_uom] / max_val
        units_max = math.floor(units_all)
        units_remaning = math.ceil(units_all - units_max)

        # Get values for max-size and remaining-size shipments (if exist)
        output = []
        if units_max > 0:
            shipment_meta = {'shipment_type': 'max-size', 'units': units_max}
            shipment_max = {}
            uom_split_ratio = max_val / shipment_values[max_uom]
            for shipment_key, shipment_value in shipment_values.items():
                if shipment_key not in do_not_split_uoms:
                    shipment_max.update({shipment_key: shipment_value * uom_split_ratio})
                else:
                    shipment_max.update({shipment_key: shipment_value})
            output.append({'meta': shipment_meta, 'shipment_values': shipment_max})
        if units_remaning > 0:
            shipment_meta = {'shipment_type': 'non-max-size', 'units': units_remaning}
            shipment_max = {}
            uom_split_ratio = (shipment_values[max_uom] - (max_val * units_max)) / shipment_values[max_uom]
            for shipment_key, shipment_value in shipment_values.items():
                if shipment_key not in do_not_split_uoms:
                    shipment_max.update({shipment_key: shipment_value * uom_split_ratio})
                else:
                    shipment_max.update({shipment_key: shipment_value})
            output.append({'meta': shipment_meta, 'shipment_values': shipment_max})
        return output

    def _get_shipment_attribute_cost(self):
        """Get all cost table details for chargeable values of a shipment (also rows not used)
        Store output df in shipments for debug"""

        for ratesheet in tqdm(self.ratesheet_scope, desc='Step 4/4. Calculating cost'.ljust(45, '.'), unit='ratesheet'):
            mask_ratesheet = (self.shipments_df_core.ratesheet_id == ratesheet.meta_ratesheet_id)
            mask_zone_exist = (self.shipments_df_core.zone.notna())
            shipments_sub_df = self.shipments_df_measures_3_chargeable[mask_ratesheet & mask_zone_exist]

            # For each shipment in shipments_sub_df we need to get chargeable measures (dict)
            for shipment_idx, shipment_row in shipments_sub_df.iterrows():
                values_chargeable = shipment_row[shipment_row.notna()].to_dict()

                # Creating ShipmentCostDetails instance in self.shipments and adding results to it
                shipment_id = self.shipments_df_core.loc[shipment_idx, 'shipment_id']
                shipment_instance = ShipmentCostDetails(shipment_id=shipment_id,
                                                        ratesheet_id=ratesheet.meta_ratesheet_id,
                                                        ratesheet_desc=f'{ratesheet.meta_trpmode}-{ratesheet.meta_carrier[:3].upper()}-{ratesheet.meta_service[:3].upper()}-{ratesheet.meta_src[14:].upper()}')
                self.shipments.append(shipment_instance)

                # Taking into consideration max_shipment_size, determine how many 'part-shipments' are (1) max-size
                # and (2) below-max-size
                shipments_parts = self._split_shipment_into_parts_based_on_max_size(values_chargeable, ratesheet.meta_max_shipment_size)

                # Iterate through shipments_parts list (can have max 2 entries) and calculate cost
                for shipment_part in shipments_parts:
                    values_chargeable = shipment_part.get('shipment_values')
                    shipment_meta = shipment_part.get('meta')

                    df_cost_details = ratesheet.cost_df.copy()
                    df_cost_details['shipment_range_values'] = df_cost_details['range_uom'].map(values_chargeable)
                    df_cost_details['shipment_cost_values'] = df_cost_details['cost_per'].map(values_chargeable)

                    zone = self.shipments_df_core.loc[shipment_idx, 'zone']
                    # Get df_cost_details
                    df_cost_details['rate'] = df_cost_details[zone]
                    df_cost_details.drop(columns=[col for col in ratesheet.cost_zones if col != zone], inplace=True)
                    mask_ranges = (df_cost_details['shipment_range_values'] > df_cost_details['range_value_from']) & (df_cost_details['shipment_range_values'] <= df_cost_details['range_value'])
                    df_cost_details.loc[mask_ranges, 'cost'] = df_cost_details['rate'] * df_cost_details['shipment_cost_values']

                    # Get df_cost_used
                    mask_cost_exist = df_cost_details.cost.notna()
                    existing_cost_types = df_cost_details[mask_cost_exist].cost_type.unique()
                    _dfs = []
                    for cost_type, behaviour in self.COST_TYPES_BEHAVIOUR.items():
                        if cost_type in existing_cost_types:
                            df_sub = df_cost_details[mask_cost_exist & (df_cost_details.cost_type == cost_type)].copy()
                            if behaviour == 'top':
                                df_sub = df_sub.loc[[df_sub.cost.idxmax()]]
                            _dfs.append(df_sub)
                    df_cost_used = pd.concat(_dfs, ignore_index=True)

                    # Get df_cost_summary
                    df_cost_summary = df_cost_used.pivot_table(values='cost', columns='cost_type', aggfunc='sum')
                    df_cost_summary = df_cost_summary.reindex(columns=self.COST_TYPES_BEHAVIOUR).fillna(0.0)
                    # Calculating final cost:
                    df_cost_summary['tot'] = np.maximum(df_cost_summary['fix'] + df_cost_summary['var'], df_cost_summary['min'])
                    df_cost_summary['fsc%'] = df_cost_summary['fsc'] * 100
                    df_cost_summary['fsc'] = df_cost_summary['tot'] * df_cost_summary['fsc']
                    df_cost_summary['tot'] += df_cost_summary['fsc'] + df_cost_summary['ext'] + df_cost_summary['lhl']
                    # Nice display
                    df_cost_summary = df_cost_summary[['tot', 'fix', 'var', 'min', 'fsc%', 'fsc', 'lhl', 'ext']]
                    col_names = {'tot': 'cost_total', 'fix': 'cost_fixed', 'var': 'cost_variable',
                                 'min': 'cost_min_charge', 'fsc%': 'fuel_surcharge-%', 'fsc': 'cost_fuel_surcharge',
                                 'lhl': 'cost_linehaul', 'ext': 'cost_extras'}
                    df_cost_summary.rename(columns=col_names, inplace=True)
                    df_cost_summary['units'] = shipment_meta.get('units')
                    df_cost_summary['part'] = f'{shipment_meta.get('shipment_type')}-units={shipment_meta.get('units')} {values_chargeable} '

                    # Adding results to shipment instance
                    shipment_instance.add_shipment_cost_data(shipment_parts=shipment_part,
                                                             df_cost_details=df_cost_details,
                                                             df_cost_used=df_cost_used,
                                                             df_cost_summary=df_cost_summary)

                # Add cost info to shipment calculated in shipment_instance.df_cost_summary (taking into account parts)
                shipment_df_cost_summary = shipment_instance.df_cost_summary.squeeze().items()
                for k, v in shipment_df_cost_summary:
                    self.shipments_df_cost.loc[shipment_idx, k] = v

    def _get_shipment_output(self):
        """Returns shipment output table"""
        df = self.shipments_df_initial
        df.rename(columns={col: f'in_{col}' for col in self.shipment_input_measures_columns}, inplace=True)

        # Add ratesheet attributes
        for ratesheet in self.ratesheet_scope:
            meta_dict = {'carrier': ratesheet.meta_carrier,
                         'trpmode': ratesheet.meta_trpmode,
                         'service': ratesheet.meta_service,
                         'src': ratesheet.meta_src}
            df.loc[df.ratesheet_id == ratesheet.meta_ratesheet_id, meta_dict.keys()] = meta_dict.values()
        df[['zone', 'leadtime']] = self.shipments_df_core[['zone', 'leadtime']]
        df_chargeables = self.shipments_df_measures_3_chargeable.rename(columns=lambda x: f'{x}_charged')
        df = pd.concat([df, self.shipments_df_measures_2_calculated, df_chargeables, self.shipments_df_cost], axis=1)

        # Put chargeable measure after measure
        cols_charged = [col for col in df.columns if col.endswith('_charged')]
        if cols_charged:
            for col in cols_charged:
                df.insert(1 + df.columns.get_loc(col.replace('_charged', '')), col, df.pop(col))

        # Status
        df['status_cost_rank'] = df.groupby('shipment_id')['cost_total'].transform(pd.Series.rank)
        df.insert(1 + df.columns.get_loc('dest_zip'), 'st_cost_rank', df.pop('status_cost_rank'))

        df['status_leadtime'] = pd.Series(np.nan, dtype='object')
        df.loc[df.status_leadtime.isna() & df.leadtime.isna(), 'status_leadtime'] = '1 (no leadtime)'
        df.loc[df.status_leadtime.isna() & df.leadtime.notna(), 'status_leadtime'] = '0 (ok)'
        df.insert(1 + df.columns.get_loc('dest_zip'), 'st_lt', df.pop('status_leadtime'))

        df['status_cost'] = pd.Series(np.nan, dtype='object')
        df.loc[df.status_cost.isna() & df.ratesheet_id.isna(), 'status_cost'] = '1 (no ratesheet)'
        df.loc[df.status_cost.isna() & df.zone.isna(), 'status_cost'] = '2 (no zone)'
        df.loc[df.status_cost.isna() & df.cost_total.isna(), 'status_cost'] = '3 (no cost)'
        df.loc[df.status_cost.isna() & df.cost_total.notna(), 'status_cost'] = '0 (ok)'
        df.insert(1 + df.columns.get_loc('dest_zip'), 'st_cost', df.pop('status_cost'))

        df['status_ratesheets_with_cost_nb'] = df.groupby('shipment_id')['cost_total'].transform('count').fillna(0)
        df.insert(1 + df.columns.get_loc('dest_zip'), 'st_#rs+cost', df.pop('status_ratesheets_with_cost_nb'))
        df['status_ratesheets_nb'] = df.groupby('shipment_id')['ratesheet_id'].transform(pd.Series.nunique).fillna(0)
        df.insert(1 + df.columns.get_loc('dest_zip'), 'st_#rs', df.pop('status_ratesheets_nb'))

        df.insert(1 + df.columns.get_loc('dest_zip'), 'ratesheet_id', df.pop('ratesheet_id'))
        df.insert(1 + df.columns.get_loc('dest_zip'), 'shipment_id', df.pop('shipment_id'))

        # Add filter mask
        filter_columns = [col for col in df.columns if col.startswith('filter_')]
        if filter_columns:
            for col in filter_columns[::-1]:
                df.insert(1 + df.columns.get_loc('dest_zip'), col, df.pop(col))
        mask_keep_for_best = pd.Series(data=True, index=df.index)
        filter_columns = [col for col in df.columns if col.startswith('filter_')]
        if filter_columns:
            for filter_column in filter_columns:
                if filter_column.replace('filter_', '') not in df.columns:
                    print(f'Filter column "{filter_column.replace('filter_', '')}" not in ratesheet meta columns and will not be used. ')
                else:
                    mask_filter = df[filter_column].isna() | (df[filter_column] == df[filter_column.replace('filter_', '')])
                    mask_keep_for_best = mask_keep_for_best & mask_filter
        df.insert(1 + df.columns.get_loc('dest_zip'), 'filter_mask', mask_keep_for_best)

        # Sort
        df.sort_values(by=['shipment_id', 'st_cost_rank'], ascending=[True, True], inplace=True)
        return df

    def _get_shipment_output_best(self):
        """Returns shipment output table with best cost (cost has rank 0) that meets the conditions"""
        df_best = self.shipments_output_details[self.shipments_output_details.filter_mask].drop_duplicates(subset='shipment_id')

        # Find shipments from shipment_input not returned in best_cost:
        missing_shipment_ids = ~self.shipment_input.shipment_id.isin(df_best.shipment_id.unique())
        df_missing_in_best = self.shipment_input[missing_shipment_ids].copy()
        total_shipments = self.shipment_input.shape[0]
        missing_shipments = df_missing_in_best.shape[0]
        if missing_shipments > 0:
            warn(f'\nThere are {missing_shipments} out of {total_shipments} shipments not included in shipment_output_best_cost.'
                 f'\nCheck table "Shipment.shipment_output_best_missing" for details.'
                 f'\nSolution: Adjust input filter (filter_src, filer_trmmode, etc) or add/change ratesheet(s).')

        # Display status
        duration = perf_counter() - self.time_start
        print(f'Processed {self.shipments_df_initial.shape[0]} shipments in {duration:0,.2f} seconds.'
              f' Shipments/second: {self.shipments_df_initial.shape[0]/duration:0,.2f}')
        return df_best, df_missing_in_best
