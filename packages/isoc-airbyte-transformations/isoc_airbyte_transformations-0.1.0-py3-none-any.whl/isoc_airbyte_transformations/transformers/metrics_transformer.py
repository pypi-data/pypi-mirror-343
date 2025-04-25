from functools import reduce
import operator
from .generic_transformer import *

class MetricsTransformer(GenericTransformer):
    def __init__(self, data):
        super().__init__(data)

    @validate_dirty
    def addition(self, transform_dict, dimetric, index, mandatory_keys):
        items = [self.data[item['stream_name']] for item in transform_dict['fields'] if isinstance(self.data[item['stream_name']], (int, float))]
        self.data[transform_dict['field_name']] = sum(items) if len(items) > 0 else 0

    @validate_dirty
    def subtraction(self, transform_dict, dimetric, index, mandatory_keys):
        items = [self.data[item['stream_name']] for item in transform_dict['fields'] if isinstance(self.data[item['stream_name']], (int, float))]
        self.data[transform_dict['field_name']] = (items[0] - sum(items[1:])) if len(items) > 0 else 0

    @validate_dirty
    def multiplication(self, transform_dict, dimetric, index, mandatory_keys):
        items = [self.data[item['stream_name']] for item in transform_dict['fields'] if isinstance(self.data[item['stream_name']], (int, float))]
        self.data[transform_dict['field_name']] = reduce(operator.mul, items) if len(items) > 0 else 0

    @validate_dirty
    def division(self, transform_dict, dimetric, index, mandatory_keys):
        items = [self.data[item['stream_name']] for item in transform_dict['fields'] if isinstance(self.data[item['stream_name']], (int, float))]
        if items[0] == 0:
            self.data[transform_dict['field_name']] = 0
        else:
            check_for_zero = [False if ii==0 else item == 0 for ii,item in enumerate(items)]
            if any(check_for_zero):
                print(f'Division by zero for {dimetric} item no {index + 1}. Skipping the transformation.')
                return
            self.data[transform_dict['field_name']] = reduce(lambda x, y: x / y, items) if len(items) > 0 else 0

    @validate_dirty
    def round_off(self, transform_dict, dimetric, index, mandatory_keys):
        self.data[transform_dict['field_name']] = round(self.data[transform_dict['fields'][0]['stream_name']], transform_dict['fields'][0]['decimals'])


