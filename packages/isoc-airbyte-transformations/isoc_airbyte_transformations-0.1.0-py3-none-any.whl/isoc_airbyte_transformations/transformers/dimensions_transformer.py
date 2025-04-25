from .generic_transformer import *

class DimensionsTransformer(GenericTransformer):
    def __init__(self, data):
        super().__init__(data)

    @validate_dirty
    def capitalize(self, transform_dict, dimetric, index, mandatory_keys):
        delimiter = transform_dict['delimiter'] if 'delimiter' in transform_dict else ' '
        items = [str(self.data[item['stream_name']]).upper() for item in transform_dict['fields']]
        self.data[transform_dict['field_name']] = delimiter.join(items)

    @validate_dirty
    def casefold(self, transform_dict, dimetric, index, mandatory_keys):
        delimiter = transform_dict['delimiter'] if 'delimiter' in transform_dict else ' '
        items = [str(self.data[item['stream_name']]).casefold() for item in transform_dict['fields']]
        self.data[transform_dict['field_name']] = delimiter.join(items)

    @validate_dirty
    def date_conversion(self, transform_dict, dimetric, index, mandatory_keys):
        root_mandatory_keys = {'format': str}
        all_present = all(key in transform_dict and isinstance(transform_dict[key], val) for key,val in root_mandatory_keys.items())
        if not all_present:
            print(f'Mandatory keys not present in the {dimetric} item no {index + 1} fields')
            return
        if 'format' not in transform_dict:
            print(f'Output date Format not present in the {dimetric} item no {index + 1} fields')
            return
        if not GenericTransformer.is_valid_date(self.data[transform_dict['fields'][0]['stream_name']], transform_dict['fields'][0]['format']):
            print(f'Date format not matches with the input given for {dimetric} item no {index + 1}.')
            return
        date_obj = datetime.strptime(self.data[transform_dict['fields'][0]['stream_name']], transform_dict['fields'][0]['format'])
        new_date_str = date_obj.strftime(transform_dict['format'])
        self.data[transform_dict['field_name']] = new_date_str
