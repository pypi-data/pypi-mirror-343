from datetime import datetime

def validate_dirty(func):
    def wrapper(self, *args, **kwargs):
        # Call hook; if it returns True, skip method
        if self.before_hook(*args, **kwargs):
            print(f"Returning without transformations for {args[2]} item no {args[2]+1}.")
            return  # You can also return a default value if needed
        return func(self, *args, **kwargs)
    return wrapper

class GenericTransformer:
    def __init__(self, data):
        self.data = data

    def before_hook(self, transform_dict, dimetric, index, mandatory_keys):
        if len(transform_dict['fields']) == 0:
            print(f'No fields provided in {dimetric} item no {index + 1}.')
            return True
        all_present = all(key in item and isinstance(item[key], val) for item in transform_dict['fields'] for key, val in mandatory_keys.items())
        if not all_present:
            print(f'Mandatory keys not present in the {dimetric} item no {index + 1} or its respective datatype is not correct.')
            return True
        mandate_conditions = [lambda x: isinstance(x, dict), lambda x: x['stream_name'] in self.data]
        dirty_list = [not cond(item) for item in transform_dict['fields'] for cond in mandate_conditions]
        if any(dirty_list):
            print(f'Invalid fields type in one of the transformation input for {dimetric} item no {index + 1}. or the transformable field is not present in the data.')
            return True
        return False

    @validate_dirty
    def concat(self, transform_dict, dimetric, index, mandatory_keys):
        delimiter = transform_dict['delimiter'] if 'delimiter' in transform_dict else ' '
        items = [str(self.data[item['stream_name']]) for item in transform_dict['fields']]
        self.data[transform_dict['field_name']] = delimiter.join(items)

    @staticmethod
    def is_valid_date(date_str, date_format):
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False