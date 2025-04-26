from pathlib import Path
import copy
from datetime import datetime

import numpy as np
import pandas as pd

from simera import Config, ZipcodeManager
from simera.utils import (
    DataInputError,
    compute_all_conversions_between_units_in_ratios,
    standardize_ratio_key,
    standardize_ratio_key_is_valid,
)

# future - sc and zm not be inside TransportRatesheet? self.sc, self.zm
sc = Config()
zm = ZipcodeManager()


class TransportRatesheet:
    def __init__(self, file_path, sheet_name):
        self.input = self._Input(file_path, sheet_name)
        self.meta = self._Meta(self.input)
        self.lane = self._Lane(self.input, self.meta)
        self.cost = self._Cost(self.input, self.meta)
        self.shortcuts = self._Shortcuts(self.lane)
        self._run_ratesheet_consistency_check()

    def __repr__(self):
        return 'TransportRatesheet'

    def _run_ratesheet_consistency_check(self):
        # All lane dest_zone are present in cost zones
        for lane_dest_zone in self.lane.zones:
            if not lane_dest_zone in self.cost.zones:
                raise DataInputError(f"Dest_zone (specified as lane) not found in cost dest_zones: '{lane_dest_zone}'.",
                                     solution=f"Make sure that '{lane_dest_zone}' is available in cost zones {self.cost.zones}.",
                                     file_path=self.input.file_path, sheet_name=self.input.sheet_name,
                                     column=f'<dest_zone> and cost_zones',
                                     values=f"<{lane_dest_zone}>")

    class _Shortcuts:
        def __init__(self, lane_trs):
            self._lane = lane_trs
            self.dest_countries = self._lane.df_dest_zone.dest_ctry.unique()

        def __repr__(self):
            return 'TransportRatesheet Shortcuts'

    class _Input:
        _INPUT_COLUMNS_DTYPES = {
            # Lane
            '<src_site>': 'string',
            '<src_region>': 'string',
            '<src_ctry>': 'string',
            '<src_zip>': 'string',
            '<src_zone>': 'string',
            '<dest_site>': 'string',
            '<dest_region>': 'string',
            '<dest_ctry>': 'string',
            '<dest_zip>': 'string',
            '<dest_zone>': 'string',
            '<transit_time>': np.float64,

            # Cost
            '<cost_type>': 'string',
            '<cost_uom>': 'string',
            '<range_value>': np.float64,
            '<range_uom>': 'string',
        }

        def __init__(self, file_path, sheet_name):
            self.file_path = file_path
            self.sheet_name = sheet_name
            self.input_data = self._read_excel_data()

        def __repr__(self):
            return f"Input(file_path='{self.file_path.parts[-1]}', sheet_name='{self.sheet_name}')"

        def _read_excel_data(self):
            # Set fixed dtypes
            dtypes = self._INPUT_COLUMNS_DTYPES.copy()

            # Read the Excel file header to get the available columns
            available_columns = pd.read_excel(io=self.file_path, sheet_name=self.sheet_name, nrows=0).columns.tolist()

            # Filter the dtype_dict to include only columns that exist in the file
            filtered_dtypes = {col: dtype for col, dtype in dtypes.items() if col in available_columns}

            # Read the Excel file with the filtered dtypes. If empty, would error would be raised.
            if filtered_dtypes:
                df = pd.read_excel(io=self.file_path, sheet_name=self.sheet_name, dtype=filtered_dtypes, engine='calamine')
            else:
                df = pd.read_excel(io=self.file_path, sheet_name=self.sheet_name, engine='calamine')

            df.dropna(how='all', inplace=True, ignore_index=True)
            return df

    class _Meta:
        def __init__(self, input_trs):
            self._input = input_trs
            self.input_data = self._get_input_data()
            self._set_initial_attributes()
            self._set_input()
            self._set_settings()
            self._set_validity()
            self._set_currency()
            self._set_service()
            self._set_src()
            self._set_dest()
            self._set_max_size(attribute='shipment_size_max')
            self._set_max_size(attribute='package_size_max')
            self._set_chargeable_ratios(attribute='chargeable_ratios')
            self._set_surcharges()
            self._set_cost_behaviour_ratesheet_and_shipments()
            self._set_custom_ratios()
            self._set_custom_defaults()

        def __repr__(self):
            return f"Meta(file_path='{self._input.file_path.parts[-1]}', sheet_name='{self._input.sheet_name}')"

        def _get_input_data(self):
            use_cols = ['<meta>', '<meta_value>']
            df = self._input.input_data.copy().reindex(columns=use_cols).dropna(subset=['<meta>'], ignore_index=True)
            df.columns = df.columns.str.replace(r'[<>]', '', regex=True)
            # Names in groups may have required indication '*' as suffix. That is removed from variable name.
            df['meta'] = df['meta'].astype('str').str.replace(r'[*]', '', regex=True)
            return df

        def _set_initial_attributes(self):
            """Convert <meta> and <meta_value> columns of ratesheet and sets all <group_name> as meta attribute.
            Meta and meta_value are converted to dict. Nan values are converter to None.
            Example: <input>'url': 'file.xlsx' it set as '.meta.input.{'url': 'file.xlsx'}'
            """

            # Get rawdata for meta
            df = self.input_data.copy()

            # Set all <groups> as meta attributes
            df_meta = df[df['meta'].str.contains('<.+>', regex=True)].copy()
            df_meta['idx_from'] = df_meta.index + 1
            df_meta['idx_to'] = (df_meta.idx_from.shift(-1) - 2).fillna(df.shape[0] - 1).astype(int)
            df_meta['meta_value'] = df_meta['meta'].str.replace(r'[<>]', '', regex=True)
            for _, row in df_meta.iterrows():
                attr_dict = df[row.idx_from:row.idx_to + 1].set_index('meta')['meta_value'].to_dict()
                # Convert all nans to None
                attr_dict_clean = {k: v if v is not None and not pd.isna(v) else None for k, v in attr_dict.items()}
                setattr(self, row.meta_value, attr_dict_clean)

        # ==============================================================================================================
        # Functions and variables
        # ==============================================================================================================
        # Get defaults and choices
        _config_choices_volume = sc.config.units_of_measure.get('choices').get('volume')
        _config_choices_weight = sc.config.units_of_measure.get('choices').get('weight')
        _config_choices_volume_and_weight = sc.config.units_of_measure.get('choices').get('volume_and_weight')

        _true_valid_choices = [True, 'True', 'TRUE', 'true', 'Yes', 'Y']
        _false_valid_choices = [False, 'False', 'FALSE', 'false', 'No', 'N']

        @classmethod
        def _bool_format_method(cls, x):
            return (True if x in cls._true_valid_choices else
                    False if x in cls._false_valid_choices else x)

        @classmethod
        def _str_upper(cls, x):
            return str.upper(str(x))

        def _set_attribute(self, group, group_item,
                           required=False,
                           default=None,
                           allowed_values: list = None,
                           format_method=None):
            """ Sets attribute values based on ratesheet input, default values and allowed options.
            group: attribute name of a group. Example: <settings>
            group_item: item in group. Example in <settings>: <ratesheet_type>
            required: if True, field can not get None
            default: value set if group_item value is np.nan/None
            allowed: list of allowed values.
            format_method: function used on item to convert it into proper dtype and format
            """

            # If group does not exist in ratesheet, create it.
            if not hasattr(self, group):
                setattr(self, group, {})
            x = getattr(self, group).get(group_item)

            # Set default
            if x is None and default is not None:
                x = default

            # Apply formatting function
            if format_method is not None and x is not None:
                x = format_method(x)

            # Check against allowed options
            if allowed_values is not None:
                if x not in allowed_values:
                    raise DataInputError(f"Invalid input for <{group}>{group_item}: {x}.",
                                         solution=f"Use one of allowed options: {allowed_values}. Check also dtypes.",
                                         file_path=self._input.file_path,
                                         sheet_name=self._input.sheet_name,
                                         column=f'<meta><{group}>{group_item}: {x}',
                                         values=x)

            # Check against required
            if required and x is None:
                raise DataInputError(f"Invalid input for <{group}>{group_item}: {x}.",
                                     solution=f"Value is required and can not return None",
                                     file_path=self._input.file_path,
                                     sheet_name=self._input.sheet_name,
                                     column=f'<meta><{group}>{group_item}: {x}',
                                     values=x)
            getattr(self, group).update({group_item: x})

        # ==============================================================================================================
        # Input
        # ==============================================================================================================
        def _set_input(self):
            self._set_attribute('input', 'file_path')
            self._set_attribute('input', 'sheet_name')

        # ==============================================================================================================
        # Settings
        # ==============================================================================================================
        def _set_settings(self):
            allowed_values = [None, 'downstream', 'mainstream']
            self._set_attribute('settings', 'ratesheet_type', default='downstream', allowed_values=allowed_values)

            allowed_values = ['starting', 'ending']
            self._set_attribute('settings', 'dest_zip_to', default='starting', allowed_values=allowed_values)

        # ==============================================================================================================
        # Validity
        # ==============================================================================================================
        def _set_validity(self):
            format_method = pd.to_datetime
            self._set_attribute('validity', 'last_update', format_method=format_method)
            self._set_attribute('validity', 'valid_from', format_method=format_method)
            self._set_attribute('validity', 'valid_to', format_method=format_method)

        # ==============================================================================================================
        # Currency
        # ==============================================================================================================
        def _set_currency(self):
            default_currency = sc.config.currency.get('default')
            self._set_attribute('currency', 'currency', default=default_currency)
            self._set_attribute('currency', 'reference_currency', default=default_currency)
            currency = getattr(self, 'currency').get('currency')
            reference_currency = getattr(self, 'currency').get('reference_currency')

            # if currency is same as default
            if currency == reference_currency:
                self._set_attribute('currency', 'rate', default=1)
                rate_logic = f'1 {reference_currency} = 1 {currency} ;)'
            else:
                try:
                    rate = sc.config.currency.get('rates').get(reference_currency).get(currency)
                except AttributeError:
                    pass
                if rate is None:
                    raise DataInputError(f"Unknown exchange rate for '{currency}' to '{reference_currency}' (set as default)",
                                         solution=f"Update 'rates':'{reference_currency}':'{currency}' "
                                         f"in simera_resources/config/currency.yaml",
                                         file_path=self._input.file_path,
                                         sheet_name=self._input.sheet_name,
                                         column=f'<meta><currency><ratesheet_currency>',
                                         values=currency)
                else:
                    self._set_attribute('currency', 'rate', default=rate)
                    rate_logic = f'1 {reference_currency} = {rate:0,.3f} {currency}, 1 {currency} = {1/rate:0,.3f} {reference_currency}'
            self._set_attribute('currency', '_rate_logic', default=rate_logic)

        # ==============================================================================================================
        # Service
        # ==============================================================================================================
        def _set_service(self):
            default_carrier = f'{self._input.sheet_name} [{datetime.now()}]'
            default_trpmode = f'{self._input.sheet_name}'
            default_service = f'{self._input.sheet_name}'
            self._set_attribute('service', 'carrier', default=default_carrier, format_method=self._str_upper)
            self._set_attribute('service', 'trpmode', default=default_trpmode, format_method=self._str_upper)
            self._set_attribute('service', 'service', default=default_service, format_method=self._str_upper)
            self._set_attribute('service', 'service1', format_method=self._str_upper)
            self._set_attribute('service', 'service2', format_method=self._str_upper)
            allowed_values = self._true_valid_choices + self._false_valid_choices
            self._set_attribute('service', 'default_ratesheet', default=True, allowed_values=allowed_values, format_method=self._bool_format_method)

        # ==============================================================================================================
        # Src - Lane Source
        # ==============================================================================================================
        def _set_src(self):
            self._set_attribute('src', 'site', format_method=self._str_upper)
            self._set_attribute('src', 'region', format_method=self._str_upper)
            self._set_attribute('src', 'ctry', format_method=self._str_upper)
            self._set_attribute('src', 'zone', format_method=self._str_upper)
            self._set_attribute('src', 'zip', format_method=self._str_upper)

        # ==============================================================================================================
        # Dest - Lane Destination
        # ==============================================================================================================
        def _set_dest(self):
            self._set_attribute('dest', 'site', format_method=self._str_upper)
            self._set_attribute('dest', 'region', format_method=self._str_upper)
            self._set_attribute('dest', 'ctry', format_method=self._str_upper)
            self._set_attribute('dest', 'zone', format_method=self._str_upper)
            self._set_attribute('dest', 'zip', format_method=self._str_upper)

        # ==============================================================================================================
        # Max Size for shipment and package
        # ==============================================================================================================
        def _set_max_size(self, attribute):
            """
            Process initial values for shipment_size_max and package_size_max and converts that into
            kg and m3. Those units will be converted to default uoms with TransportRatesheetManager.
            :param attribute: shipment_size_max or package_size_max
            :return: None (set shipment_size_max and package_size_max dicts as attribute to ratesheet meta)
            """

            # If attribute (e.g. shipment_size_max) is not in ratesheet, set it up with empty dict as value
            if not hasattr(self, attribute):
                setattr(self, attribute, {})

            # Get initial values for attribute (if exist). If ratesheet has uoms not in choices, raise error.
            volume_init = {}
            weight_init = {}
            for uom, value in getattr(self, attribute).items():
                # Check if uom is in choices. If not, raise
                # error
                if uom not in self._config_choices_volume_and_weight:
                    raise DataInputError(f"Invalid Unit '{uom}' for '<{attribute}>'. "
                                         f"Avail. weight & volume choices: '{self._config_choices_volume_and_weight}'",
                                         solution=f"Set correct unit",
                                         file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                         column='<meta>',
                                         values=f"<{attribute}>{uom}: {value}")
                if uom in self._config_choices_volume and value is not None:
                    volume_init.update({uom: value})
                if uom in self._config_choices_weight and value is not None:
                    weight_init.update({uom: value})

            # Calculate values for weight and volume in kg and m3
            volume_converted_to_m3 = {f'{k} => m3': round(
                v / sc.config.units_of_measure['conversions']['volume'][k]['m3'], 5) for k, v in
                volume_init.items()}
            weight_converted_to_kg = {f'{k} => kg': round(
                v / sc.config.units_of_measure['conversions']['weight'][k]['kg'], 5) for k, v in
                weight_init.items()}

            # Get minimum values for shipment size (if more than 1 value provided for uom)
            volume_size = min(volume_converted_to_m3.values()) if volume_converted_to_m3 else None
            weight_size = min(weight_converted_to_kg.values()) if weight_converted_to_kg else None

            # Set attributes that will be used in script
            setattr(self, attribute, {'m3': volume_size})
            getattr(self, attribute).update({'kg': weight_size})
            getattr(self, attribute).update({'_origin': 'Ratesheet'})
            volume_msg = f'Ratesheet: {volume_converted_to_m3}' if volume_converted_to_m3 else None
            getattr(self, attribute).update({'_volume_ratesheet_input': volume_init})
            getattr(self, attribute).update({'_volume_ratesheet_calculation': volume_msg})
            weight_msg = f'Ratesheet: {weight_converted_to_kg}' if weight_converted_to_kg else None
            getattr(self, attribute).update({'_weight_ratesheet_input': weight_init})
            getattr(self, attribute).update({'_weight_ratesheet_calculation': weight_msg})

            # If volume & weights are None, get values based on transport_ratesheet.yaml config file (if exist)
            ratesheet_trpmode = getattr(self, 'service').get('trpmode')
            if getattr(self, attribute)['m3'] is None and getattr(self, attribute)['kg'] is None:
                try:
                    volume = sc.config.transport_ratesheet.get(attribute).get(ratesheet_trpmode).get('m3')
                    if volume is not None:
                        getattr(self, attribute).update({'m3': volume})
                        getattr(self, attribute).update({'_origin': 'Config'})
                    getattr(self, attribute).update({'_volume_config_input': sc.config.transport_ratesheet.get(attribute).get(ratesheet_trpmode).get('_volume_config_input')})
                    getattr(self, attribute).update({'_volume_config_calculation': sc.config.transport_ratesheet.get(attribute).get(ratesheet_trpmode).get('_volume_config_calculation')})
                except AttributeError:  # Transport mode in config may not be present
                    pass

                try:
                    weight = sc.config.transport_ratesheet.get(attribute).get(ratesheet_trpmode).get('kg')
                    if weight is not None:
                        getattr(self, attribute).update({'kg': weight})
                        getattr(self, attribute).update({'_origin': 'Config'})
                    getattr(self, attribute).update({'_weight_config_input': sc.config.transport_ratesheet.get(attribute).get(ratesheet_trpmode).get('_weight_config_input')})
                    getattr(self, attribute).update({'_weight_config_calculation': sc.config.transport_ratesheet.get(attribute).get(ratesheet_trpmode).get('_weight_config_calculation')})
                except AttributeError:  # Transport mode in config may not be present
                    pass

        # ==============================================================================================================
        # Chargeable ratios
        # ==============================================================================================================
        def _set_chargeable_ratios(self, attribute='chargeable_ratios'):
            # Check: Attribute not in ratesheet, set it up with empty dict
            if not hasattr(self, attribute):
                setattr(self, attribute, {})

            # Check: Only one entry allowed with a non-None/non-NaN value.
            chargeable_ratios_init = getattr(self, attribute).copy()
            if chargeable_ratios_init:
                nb_valid_ratios = sum(1 for v in chargeable_ratios_init.values() if v is not None)
                if nb_valid_ratios > 1:
                    _wrong_ratios = {k: v for k, v in chargeable_ratios_init.items() if v is not None}
                    raise DataInputError(
                        f"Only one chargeable ratio allowed (with value). Received {nb_valid_ratios} ratios with values: {_wrong_ratios}.",
                        solution=f"Use value for only one ratio.",
                        file_path=self._input.file_path,
                        sheet_name=self._input.sheet_name,
                        column="<meta>",
                        values=f"<{attribute}><{chargeable_ratios_init}>"
                    )

            # Classify initial ratios to correct/incorrect. Only correct will be processed.
            ratios_correct = {}
            ratios_incorrect = {}
            for k, v in chargeable_ratios_init.items():
                if v is not None:
                    ratios_correct.update({k: v})
                else:
                    ratios_incorrect.update({k: None})

            # Check: ratio is proper format 'x/y'
            if ratios_correct:
                k = list(ratios_correct.keys())[-1]
                k_converted = standardize_ratio_key(k)
                if not standardize_ratio_key_is_valid(k_converted):
                    raise DataInputError(f"Incorrect format for chargeable ratio: '{k}'.",
                                         solution=f"Proper format examples: `m3 per kg`, 'in3/lb', 'cft / kg'.",
                                         file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                         column=f'<meta><{attribute}>',
                                         values=f"<{k}>")

            # Generate ratio conversions for ratios_correct
            ratio_conversions = compute_all_conversions_between_units_in_ratios(ratios_correct, include_self=False)

            # Classify uom for weight_uom, volume_uom, ratio_uom
            if ratio_conversions:
                volume_uom = [uom for uom in ratio_conversions if uom in self._config_choices_volume]
                weight_uom = [uom for uom in ratio_conversions if uom in self._config_choices_weight]

                if not volume_uom or not weight_uom:
                    raise DataInputError(f"Incorrect units for ratios. Proper volume units: {volume_uom}. Proper weight units: {weight_uom}.",
                                         solution=f"Proper ratio format: volume/weight or weight/volume (E.g.: 'kg per m3', 'in3/lb'. Allowed units: {self._config_choices_volume_and_weight}",
                                         file_path=self._input.file_path,
                                         sheet_name=self._input.sheet_name,
                                         column="<meta>",
                                         values=f"<{attribute}>{chargeable_ratios_init}")

                volume_uom = volume_uom[-1]
                weight_uom = weight_uom[-1]

                # Calculate fixed unit ratio kg/m3 (independent of input)
                weight_to_volume_value_correct_ratio = ratio_conversions[weight_uom][volume_uom]
                # Get ratios to kg and m3
                ratio_to_m3 = sc.config.units_of_measure['conversions']['volume'][volume_uom]['m3']
                ratio_to_kg = sc.config.units_of_measure['conversions']['weight'][weight_uom]['kg']
                kg_to_m3_ratio = (weight_to_volume_value_correct_ratio / ratio_to_kg) * ratio_to_m3
            else:
                kg_to_m3_ratio = None

            setattr(self, attribute, {'kg/m3': kg_to_m3_ratio})
            getattr(self, attribute).update({'_ratesheet_input': {'correct': ratios_correct, 'skipped': ratios_incorrect}})
            getattr(self, attribute).update({'_ratesheet_calculation': f"Ratesheet: {ratios_correct} => 'kg/m3': {kg_to_m3_ratio}"})

        # ==============================================================================================================
        # Surcharges
        # ==============================================================================================================
        def _set_surcharges(self):
            self._set_attribute('surcharges', 'fuel_surcharge', default=0, format_method=float)

        # ==============================================================================================================
        # Cost Types Behaviour in Ratesheets and Shipments
        # ==============================================================================================================
        def _set_cost_behaviour_ratesheet_and_shipments(self):
            attributes = ['cost_behaviour_ratesheet', 'cost_behaviour_shipment']
            for attribute in attributes:
                allowed_values = ['max', 'min', 'sum']
                default_behaviour = 'sum'

                # Set and check default cost types
                default_cost_types = {
                    'min': 'max',
                    'fix': 'sum',
                    'var': 'sum',
                    'lhl': 'sum',
                }
                for cost_type, behaviour in default_cost_types.items():
                    self._set_attribute(attribute, cost_type, default=behaviour, format_method=str, allowed_values=allowed_values)

                # Fill custom cost_types with None input
                for cost_type, behaviour in getattr(self, attribute).items():
                    if cost_type not in default_cost_types.keys():
                        self._set_attribute(attribute, cost_type, default=default_behaviour, format_method=str, allowed_values=allowed_values)


        # ==============================================================================================================
        # Custom ratios
        # ==============================================================================================================
        def _set_custom_ratios(self, attribute='custom_ratios'):
            # If not in ratesheet, make empty dict.
            if not hasattr(self, attribute):
                setattr(self, attribute, {})
            ratesheet_input = getattr(self, attribute)

            # Remove attributes
            setattr(self, attribute, {})

            # Check if ratio is valid
            if ratesheet_input:
                for k, v in ratesheet_input.items():
                    if not standardize_ratio_key_is_valid(standardize_ratio_key(k)):
                        raise DataInputError(f"Incorrect format for custom ratio: '{k}'.",
                                             solution=f"Proper format examples: `m3 per kg`, 'in3/lb', 'cft / kg'.",
                                             file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                             column=f'<meta><{attribute}>',
                                             values=f"<{k}>")

            # Get all conversions for custom_ratios
            ratesheet_input_converted = compute_all_conversions_between_units_in_ratios(ratesheet_input, keep_none=False)

            # Get config input
            config_input = sc.config.transport_ratesheet.get('custom_ratios').copy()
            config_input_updated = copy.deepcopy(config_input)

            # Overwrite config with ratesheet input
            for k_trs, v_trs in ratesheet_input_converted.items():
                if config_input_updated.get(k_trs) is not None:
                    config_input_updated.get(k_trs).update(v_trs)
                else:
                    config_input_updated.update({k_trs: v_trs})

            # setattr(self, attribute, compute_all_conversions_between_units_in_ratios(ratios_init))
            getattr(self, attribute).update(config_input_updated)
            getattr(self, attribute).update({'_ratesheet_input': ratesheet_input})
            getattr(self, attribute).update({'_ratesheet_input_converted': ratesheet_input_converted})
            getattr(self, attribute).update({'_config_input_init': config_input})

        # ==============================================================================================================
        # Custom defaults
        # ==============================================================================================================
        def _set_custom_defaults(self, attribute='custom_defaults'):
            # If not in ratesheet, make empty dict.
            if not hasattr(self, attribute):
                setattr(self, attribute, {})
            ratesheet_input = getattr(self, attribute)

            # Remove attributes
            setattr(self, attribute, {})

            # Check if ratio is valid
            if ratesheet_input:
                for k, v in ratesheet_input.items():
                    if v is None:
                        raise DataInputError(f"Incorrect value for custom default: '{k}'.",
                                             solution=f"Value can not be None",
                                             file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                             column=f'<meta><{attribute}>',
                                             values=f"<{k}>")

            # Get config input
            config_input = sc.config.transport_ratesheet.get('custom_defaults').copy()
            config_input_updated = copy.deepcopy(config_input)

            # Overwrite config with ratesheet input
            config_input_updated.update(ratesheet_input)

            # setattr(self, attribute, compute_all_conversions_between_units_in_ratios(ratios_init))
            getattr(self, attribute).update(config_input_updated)
            getattr(self, attribute).update({'_ratesheet_input': ratesheet_input})
            getattr(self, attribute).update({'_config_input_init': config_input})

    class _Lane:
        def __init__(self, input_trs, meta_trs):
            self._input = input_trs
            self._meta = meta_trs
            self.input_data = self._get_input_data()
            self.output_data = self._normalize_input_data()
            self.df_dest_zone = self._set_df_dest_zone()
            self.df_transit_time = self._set_df_transit_time()
            self._set_extra_attributes()

        def __repr__(self):
            return f"Lane(file_path='{self._input.file_path.parts[-1]}', sheet_name='{self._input.sheet_name}')"

        def _get_input_data(self):
            # future - all <src_> and <dest_> will be included
            #  use_cols = list(self._input._LANE_COLUMNS_DTYPES.keys())
            use_cols = ['<dest_ctry>', '<dest_zip>', '<dest_zone>', '<transit_time>']
            df = self._input.input_data.copy().reindex(columns=use_cols).dropna(how='all', ignore_index=True)
            df.columns = df.columns.str.replace(r'[<>]', '', regex=True)
            if df.shape[0] == 0:
                raise DataInputError(f"Missing TransportRatesheet Lane input.",
                                     solution=f"At least one row of data is required with <dest_ctry>.",
                                     file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                     column=f'<dest_ctry>',
                                     values=f"Example: 'PL'")
            return df

        def _normalize_input_data(self):
            # Classify and normalize data
            df = self.input_data.copy()

            # Country of destination '<dest_ctry>' must be always provided
            if df.dest_ctry.isna().any():
                raise DataInputError(f"Missing Country <dest_ctry> in TransportRatesheet Lane input.",
                                     solution=f"Column <dest_ctry> can not be empty if other columns are filled.",
                                     file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                     column=f'<dest_ctry>',
                                     values=f"\n{df[df.dest_ctry.isna()]}")

                # Classify input based on provided data
            df['input_structure'] = df.apply(lambda row: row['dest_ctry'] + ', ' + ', '.join([col for col in df.columns if pd.notna(row[col])]), axis=1)
            df['input_structure'] = df['input_structure'].map({v: f'{i}. {v}' for i, v in enumerate(df['input_structure'].unique())})
            df['input_structure'] = df['input_structure'].astype('string')

            # Step0. Exception for parcel: If only country is provided (and zone is missing), set zone as country
            df.loc[df.dest_zip.isna() & df.dest_zone.isna() & df.transit_time.isna(), 'dest_zone'] = df.dest_ctry

            # Step1. Remove entries where both dest_zone and transit_time are NaN
            mask = df.dest_zone.isna() & df.transit_time.isna()
            df = df.loc[~mask].copy()
            if df.empty:
                raise DataInputError(f"TransportRatesheet does not have any valid input for Lane.",
                                     solution=f"Provide at least single valid row of data (with zone or transit_time).",
                                     file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                     column=f'<dest_ctry><dest_zip><dest_zone><transit_time>')

            # Step2. Replace NaN dest_zip with first zipcode for given country
            df.rename(columns={'dest_zip': 'dest_zip_init'}, inplace=True)
            df['dest_zip'] = df.dest_zip_init
            df.loc[df.dest_zip.isna(), 'dest_zip'] = df.dest_ctry.map(zm.zipcode_clean_first)

            # Step3. Clean zipcode input before allocation to list or range
            # Replace list indicators ';' or '.' with comma
            df['dest_zip'] = df['dest_zip'].str.replace(r'[;.]', ',', regex=True)
            # Keep only a-z, A_Z, 0-9, '-', ','
            df['dest_zip'] = df['dest_zip'].str.replace(r'[^a-zA-Z0-9,-]', '', regex=True)
            # Remove ',' if no chars/number follows it
            df['dest_zip'] = df['dest_zip'].str.replace(r',(?=\s|$|[^a-zA-Z0-9])', '', regex=True)

            # Step4. Expand zipcode input as list (create new rows)
            df['dest_zip'] = df['dest_zip'].str.split(',')
            df = df.explode('dest_zip').reset_index(drop=True)
            df['dest_zip'] = df['dest_zip'].astype('string')
            # Note: Sorting with input_structure is essential to maintain integrity (difference vs previous version)
            df.sort_values(by=['dest_ctry', 'input_structure', 'dest_zip'], inplace=True)

            # Step5. Converts dest_zip to range (zip_from, zip_to). If input is range, split it. If not, zip_to is ps.NA
            df['dest_zip_as_range'] = df['dest_zip'].str.contains(rf'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$')
            df['clean_first'] = df.dest_ctry.map(zm.zipcode_clean_first).astype('string')
            df['clean_last'] = df.dest_ctry.map(zm.zipcode_clean_last).astype('string')
            if df['dest_zip_as_range'].any():  # Without this check, error is raised as only one item exist in list
                df[['dest_zip_from', 'dest_zip_to']] = df['dest_zip'].str.split('-', expand=True).fillna(pd.NA)
            else:
                df['dest_zip_from'] = df['dest_zip']
                df['dest_zip_to'] = pd.NA
                df['dest_zip_to'] = df['dest_zip_to'].astype("string")
            df.loc[df['dest_zip_to'].isna(), 'dest_zip_to'] = df.groupby(['dest_ctry', 'input_structure'])['dest_zip_from'].transform(pd.Series.shift, -1).fillna(np.nan)

            # Step6. Get zip_to range meta (starting or ending).
            df['dest_zip_to_meta'] = self._meta.settings.get('dest_zip_to')
            df['dest_zip_to_meta'] = df['dest_zip_to_meta'].astype('string')
            df.loc[~df.dest_zip_as_range, 'dest_zip_to_meta'] = 'ending'

            # Step7: 'dest_zip_from' as full format (99999: 00-10 -> 00000-...; 10-20 -> 10000-...)
            df['dest_zip_from_clean'] = df.apply(lambda row: zm.clean_zipcode(row['dest_ctry'], row['dest_zip_from']), axis=1)
            df['dest_zip_from_clean'] = df['dest_zip_from_clean'].astype('string')

            # Step8: 'dest_zip_to' with 'starting' as full format (99999: 00-10 -> ...-10999; 10-20 -> ...-20999)
            mask = df.dest_zip_to.notna() & (df.dest_zip_to_meta == 'starting')
            df.loc[mask, 'dest_zip_to_clean'] = df.loc[mask].apply(lambda row: zm.clean_zipcode(row['dest_ctry'], row['dest_zip_to'], variant='last'), axis=1)
            df['dest_zip_to_clean'] = df['dest_zip_to_clean'].astype('string')

            # Step9: 'dest_zip_to' with 'ending' as full format (99999: 00-10 -> ...-09999; 10-20 -> ...-19999)
            mask = df.dest_zip_to.notna() & (df.dest_zip_to_meta == 'ending')
            df.loc[mask, 'dest_zip_to_clean'] = df.loc[mask].apply(lambda row: zm.clean_zipcode(row['dest_ctry'], row['dest_zip_to']), axis=1)
            df.loc[mask, 'dest_zip_to_clean'] = df.loc[mask].apply(lambda row: zm.adjacent_zipcode(row['dest_ctry'], row['dest_zip_to_clean'], direction='previous'), axis=1)

            # Step10. Special case when input is given as all zipcodes in full length (PL - 00000, 00001, ..., 99999)
            #  Turns out it's not needed. For now at least.


            # Step11: 'dest_zip_to' with 'ending' & pd.NA as last full format
            #  (99999: 00-NA -> ...-99999; 10-NA -> ...-99999)
            mask = df.dest_zip_to_clean.isna()
            df.loc[mask, 'dest_zip_to_clean'] = df['clean_last']

            # Step12 - Make sure that 'clean_first' and 'clean_last' in included in zipcode ranges per 'input_structure'
            # Typically, ratesheets start with '01' or '10' (so not include first clean zip). May also not include last.
            # Note: this does not exist in previous version.
            gr = df.groupby(['dest_ctry', 'input_structure'], as_index=False)[['dest_zip_from_clean', 'dest_zip_to_clean', 'clean_first', 'clean_last']].agg({'dest_zip_from_clean': 'min', 'dest_zip_to_clean': 'max', 'clean_first': 'first', 'clean_last': 'first'})

            mask = gr.clean_first < gr.dest_zip_from_clean
            if not gr.loc[mask].empty:
                gr.loc[mask, 'from_first'] = gr.clean_first
                gr.loc[mask, 'from_last'] = gr.loc[mask].apply(lambda row: zm.adjacent_zipcode(row['dest_ctry'], row['dest_zip_from_clean'], direction='previous'), axis=1)
                gr.loc[mask, 'extra_from_range'] = gr.from_first + '-' + gr.from_last
                gr_first = gr.loc[mask, ['input_structure', 'dest_zip_from_clean', 'extra_from_range']].copy()

                df = df.merge(gr_first, how='left', on=['input_structure', 'dest_zip_from_clean'])
                mask = df.extra_from_range.notna()
                df.loc[mask, 'dest_zip_from_clean'] = df.loc[mask, 'extra_from_range'] + ',' + df.loc[mask, 'dest_zip_from_clean']
                df['dest_zip_from_clean'] = df['dest_zip_from_clean'].str.split(',')
                df = df.explode('dest_zip_from_clean').reset_index(drop=True)
                df['dest_zip_from_clean'] = df['dest_zip_from_clean'].astype('string')
                mask_range = df['dest_zip_from_clean'].str.contains(rf'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$', na=False)
                df.loc[mask_range, ['dest_zip_from_clean', 'dest_zip_to_clean']] = df.loc[mask_range, 'dest_zip_from_clean'].str.split('-', expand=True).values
                df.loc[mask_range, 'extra_from_range'] += ' (added)'
                df.loc[df.extra_from_range.notna() & ~df.extra_from_range.str.contains('added'), 'extra_from_range'] += ' (input)'

            mask = gr.clean_last > gr.dest_zip_to_clean
            if not gr.loc[mask].empty:
                gr.loc[mask, 'to_first'] = gr.loc[mask].apply(lambda row: zm.adjacent_zipcode(row['dest_ctry'], row['dest_zip_to_clean'], direction='next'), axis=1)
                gr.loc[mask, 'to_last'] = gr.clean_last
                gr.loc[mask, 'extra_to_range'] = gr.to_first + '-' + gr.to_last
                gr_last = gr.loc[mask, ['input_structure', 'dest_zip_to_clean', 'extra_to_range']].copy()

                df = df.merge(gr_last, how='left', on=['input_structure', 'dest_zip_to_clean'])
                mask = df.extra_to_range.notna()
                df.loc[mask, 'dest_zip_to_clean'] = df.loc[mask, 'dest_zip_to_clean'] + ',' + df.loc[mask, 'extra_to_range']
                df['dest_zip_to_clean'] = df['dest_zip_to_clean'].str.split(',')
                df = df.explode('dest_zip_to_clean').reset_index(drop=True)
                df['dest_zip_to_clean'] = df['dest_zip_to_clean'].astype('string')
                mask_range = df['dest_zip_to_clean'].str.contains(rf'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$', na=False)
                df.loc[mask_range, ['dest_zip_from_clean', 'dest_zip_to_clean']] = df.loc[mask_range, 'dest_zip_to_clean'].str.split('-', expand=True).values
                df.loc[mask_range, 'extra_to_range'] += ' (added)'
                df.loc[df.extra_to_range.notna() & ~df.extra_to_range.str.contains('added'), 'extra_to_range'] += ' (input)'

            return df

        def _set_df_dest_zone(self):
            # Final version for dest zone
            mask_zone = self.output_data.dest_zone.notna()
            columns_zone = ['dest_ctry', 'dest_zip_from_clean', 'dest_zip_to_clean', 'dest_zone']
            df = self.output_data.loc[mask_zone, columns_zone].copy()
            df.rename(columns={'dest_zip_from_clean': 'dest_zip_from', 'dest_zip_to_clean': 'dest_zip_to'}, inplace=True)
            return df

        def _set_df_transit_time(self):
            # Final version for dest zone
            mask_zone = self.output_data.transit_time.notna()
            columns_transit_time = ['dest_ctry', 'dest_zip_from_clean', 'dest_zip_to_clean', 'transit_time']
            df = self.output_data.loc[mask_zone, columns_transit_time].copy()
            df.rename(columns={'dest_zip_from_clean': 'dest_zip_from', 'dest_zip_to_clean': 'dest_zip_to'}, inplace=True)
            return df

        def _set_extra_attributes(self):
            setattr(self, 'zones', list(self.df_dest_zone.dest_zone.unique()))

    class _Cost:
        _COST_META_COLUMNS = ['<cost_type>', '<cost_uom>', '<range_value>', '<range_uom>']
        _DEFAULT_MISSING_RANGE_VALUE = 99999999
        _DEFAULT_MISSING_UOM = 'm3'

        def __init__(self, input_trs, meta_trs):
            self._input = input_trs
            self._meta = meta_trs
            self.input_data = self._get_input_data()
            self.zones = self._get_zones()
            self.cost_types = self._get_cost_type_and_set_behaviour()
            self.df_cost = self._normalize_input_data()

        def __repr__(self):
            return f"Cost(file_path='{self._input.file_path.parts[-1]}', sheet_name='{self._input.sheet_name}')"

        def _get_input_data(self):
            # Get names of columns for cost
            columns_cost = self._COST_META_COLUMNS[:]
            columns_zone = [col for col in self._input.input_data.columns[self._input.input_data.columns.get_loc('<range_uom>') + 1:] if not col.startswith('Unnamed:')]
            columns_cost.extend(columns_zone)

            # Drop empty rows
            df = self._input.input_data.copy().reindex(columns=columns_cost).dropna(how='all', ignore_index=True)

            # Change zone columns to numeric
            for col in df[columns_zone].select_dtypes(include=['object', 'string']).columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Drop empty columns
            df = df.dropna(axis=1, how='all', ignore_index=True)

            df.columns = df.columns.astype('string')
            df.columns = df.columns.str.replace(r'[<>]', '', regex=True)

            if df.empty:
                raise DataInputError(f"Missing TransportRatesheet Cost input.",
                                     solution=f"At least one row of data is required",
                                     file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                     column=f'{columns_cost}')
            return df

        def _get_zones(self):
            cost_columns_strip = [col.strip('<>') for col in self._COST_META_COLUMNS]
            return [col for col in self.input_data.columns if col not in cost_columns_strip]

        def _get_cost_type_and_set_behaviour(self):
            cost_types = self.input_data['cost_type'].unique()
            new_cost_types_ratesheet = [cost for cost in cost_types if cost not in self._meta.cost_behaviour_ratesheet]
            new_cost_types_shipment = [cost for cost in cost_types if cost not in self._meta.cost_behaviour_shipment]
            # If new cost_types ware found, add them to cost_behaviours and rerun set function to overwrite None values
            if new_cost_types_shipment or new_cost_types_ratesheet:
                self._meta.cost_behaviour_ratesheet.update(dict.fromkeys(new_cost_types_ratesheet))
                self._meta.cost_behaviour_shipment.update(dict.fromkeys(new_cost_types_shipment))
                # Execute once again cost_behaviour
                # noinspection PyProtectedMember
                self._meta._set_cost_behaviour_ratesheet_and_shipments()
            return list(cost_types)

        def _normalize_input_data(self):
            df = self.input_data.copy()

            # Convert cost input to reference currency
            setattr(self, 'currency', {
                'input_currency': self._meta.currency.get('currency'),
                'output_currency': self._meta.currency.get('reference_currency'),
            })
            df[self.zones] /= self._meta.currency.get('rate')

            # Missing range values and uom are filled with defaults
            df['range_value'] = df.range_value.fillna(self._DEFAULT_MISSING_RANGE_VALUE)
            df['range_uom'] = df.range_uom.fillna(self._DEFAULT_MISSING_UOM)

            # Add 'range_value_from' for lookup in ShipmentCost
            # Categorical is used for sorting only (to keep same sequence)
            df['cost_type'] = pd.Categorical(df['cost_type'], categories=df.cost_type.drop_duplicates(), ordered=True)
            df.drop_duplicates(['cost_type', 'range_value'], keep='first', inplace=True)
            df.sort_values(by=['cost_type', 'range_value'], inplace=True)
            df.insert(df.columns.get_loc('range_value'), 'range_value_from', df.groupby(['cost_type'], observed=True)['range_value'].transform(pd.Series.shift, 1).fillna(0))
            df['cost_type'] = df.cost_type.astype('string')
            df.rename(columns={'range_value': 'range_value_to'}, inplace=True)

            # ==========================================================================================================
            # Check if all potentially needed UoMs are provided. This is in case ratios are needed and not specified on
            #  shipment level.
            # ==========================================================================================================
            # Step1 - Convert weight and volume uoms to 'kg' and 'm3'
            # cost_uom change cost in zones
            for cost_uom in df.cost_uom.unique():
                # if cost_uom in volume
                default_volume = 'm3'
                if cost_uom in sc.config.units_of_measure.get('choices').get('volume') and cost_uom != default_volume:
                    mask = (df.cost_uom == cost_uom)
                    df.loc[mask, 'cost_uom'] = default_volume
                    df.loc[mask, self.zones] *= sc.config.units_of_measure.get('conversions').get('volume').get(cost_uom).get(default_volume)
                # if cost_uom in weight
                default_weight = 'kg'
                if cost_uom in sc.config.units_of_measure.get('choices').get('weight') and cost_uom != default_weight:
                    mask = (df.cost_uom == cost_uom)
                    df.loc[mask, 'cost_uom'] = default_weight
                    df.loc[mask, self.zones] *= sc.config.units_of_measure.get('conversions').get('weight').get(cost_uom).get(default_weight)
            # range_uom change cost in zones
            for range_uom in df.range_uom.unique():
                # if range_uom in volume
                default_volume = 'm3'
                if range_uom in sc.config.units_of_measure.get('choices').get('volume') and range_uom != default_volume:
                    mask = (df.range_uom == range_uom)
                    df.loc[mask, 'range_uom'] = default_volume
                    df.loc[mask, 'range_value_to'] /= sc.config.units_of_measure.get('conversions').get('volume').get(range_uom).get(default_volume)
                # if range_uom in weight
                default_weight = 'kg'
                if range_uom in sc.config.units_of_measure.get('choices').get('weight') and range_uom != default_weight:
                    mask = (df.range_uom == range_uom)
                    df.loc[mask, 'range_uom'] = default_weight
                    df.loc[mask, 'range_value_to'] /= sc.config.units_of_measure.get('conversions').get('weight').get(range_uom).get(default_weight)
                    df.loc[mask, 'range_value_from'] /= sc.config.units_of_measure.get('conversions').get('weight').get(range_uom).get(default_weight)

            # ==========================================================================================================
            # Step2 - Determine quantities/drivers (for cost and range uoms)
            # There are 2 options to get driver value.
            # 1. From meta.custom_ratios (best works with volume, kg, pallets, etc.)
            # 2. from meta.custom_defaults (best for surcharges like shipment, drop, long_prod, whs operations, etc.)
            # If driver is not given in one of the two, error will be raised to add it.
            # ==========================================================================================================
            # Get all
            uoms = list(pd.unique(df[['cost_uom', 'range_uom']].values.ravel()))
            setattr(self, 'uoms', uoms)
            for uom in uoms:
                if uom not in self._meta.custom_ratios and uom not in self._meta.custom_defaults:
                    raise DataInputError(f"Missing default quantity driver for ratesheet UOM: '{uom}'.",
                                         solution=f"Add value to <custom_ratios> e.g. '{uom}/m3=1' or to <custom_defaults> e.g. '{uom}=0'",
                                         file_path=self._input.file_path, sheet_name=self._input.sheet_name,
                                         column=f'<meta><custom_ratios>|<custom_defaults>',
                                         values=f"<{uom}>")
            return df


if __name__ == '__main__':
    test_dir = Path(r'C:\Users\plr03474\NoOneDrive\Python\Simera\simera_inputs\transport')
    test_rs = 'Simera Transport Ratesheet Template_v0.4.5.xlsb'
    test_file = test_dir / test_rs
    # test_worksheet = "_0.4.1"
    test_worksheet = "tester"

    trs = TransportRatesheet(test_file, test_worksheet)
    # trs.cost.df_data.to_clipboard(index=False)

    # future - zone aggregate results for zip and zones if possible
