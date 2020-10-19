import json

from fwf_parser.errors.invalid_spec_error import InvalidSpecError

REQUIRED_SPECS = ['Offsets', 'FixedWidthEncoding', 'DelimitedEncoding']

def read_spec(spec_file):

    with open(spec_file, 'r') as jsonfile:
        spec = json.load(jsonfile)

        if not set(REQUIRED_SPECS).issubset(set(spec)):
            raise InvalidSpecError('Spec requires `Offsets`, `FixedWidthEncoding` and `DelimitedEncoding`!')
        
        offsets = [int(offset) for offset in spec['Offsets']]
        return {
            "input_encoding": spec['FixedWidthEncoding'],
            "offsets": offsets,
            "line_width": sum(offsets),
            "output_encoding": spec['DelimitedEncoding']
        }
