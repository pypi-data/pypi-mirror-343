from .transformers.dimensions_transformer import DimensionsTransformer
from .transformers.metrics_transformer import MetricsTransformer


class IsocAirbyteTransformations:
    def __init__(self, data, rules):
        self.data = data
        self.rules = rules
        dimensions_transformer = DimensionsTransformer(self.data)
        metrics_transformer = MetricsTransformer(self.data)
        self.mandatory_keys = {'operation': str, 'field_name': str, 'fields': list}
        self.operations = {
            'Concat': {'func': dimensions_transformer.concat, 'mandatory_keys': {'stream_name': str}},
            'Upper Case': {'func': dimensions_transformer.capitalize, 'mandatory_keys': {'stream_name': str}},
            'Lower Case': {'func': dimensions_transformer.casefold, 'mandatory_keys': {'stream_name': str}},
            'Date Trunc': {'func': dimensions_transformer.date_conversion, 'mandatory_keys': {'stream_name': str, 'format': str}},
            'Extract Month': {'func': dimensions_transformer.date_conversion, 'mandatory_keys': {'stream_name': str, 'format': str}},
            'Extract Year': {'func': dimensions_transformer.date_conversion, 'mandatory_keys': {'stream_name': str, 'format': str}},
            'Addition': {'func': metrics_transformer.addition, 'mandatory_keys': {'stream_name': str}},
            'Subtraction': {'func': metrics_transformer.subtraction, 'mandatory_keys': {'stream_name': str}},
            'Multiplication': {'func': metrics_transformer.multiplication, 'mandatory_keys': {'stream_name': str}},
            'Division': {'func': metrics_transformer.division, 'mandatory_keys': {'stream_name': str}},
            'Round Off': {'func': metrics_transformer.round_off, 'mandatory_keys': {'stream_name': str, 'decimals': int}},
        }


    def transform(self):
        dimensions_transform_rules = self.rules['dimensions'] if 'dimensions' in self.rules else []
        metrics_transform_rules = self.rules['metrics'] if 'metrics' in self.rules else []
        combined_rules = ([(item, 'dimension', ii) for ii, item in enumerate(dimensions_transform_rules)] +
                          [(item, 'metric', ii) for ii, item in enumerate(metrics_transform_rules)])
        for transform, dimetric, index in combined_rules:
            all_present = all(key in transform and isinstance(transform[key], val) for key, val in self.mandatory_keys.items())
            if not all_present:
                print(f'Mandatory keys not present in the {dimetric} item no {index + 1} or its respective datatype is not correct.')
                continue
            if transform['operation'] not in self.operations:
                print(f'Requested transformation is not in the scope for the {dimetric} item no {index + 1}. '
                      'Please update the package to apply the requested transformation.')
                continue
            try:
                self.operations[transform['operation']]['func'](transform, dimetric, index, self.operations[transform['operation']]['mandatory_keys'])
            except Exception as TransformationError:
                print(TransformationError)
