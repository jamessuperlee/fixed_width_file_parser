import json

from fwf_parser.spec import Spec
from fwf_parser.errors.missing_spec_error import MissingSpecError
from fwf_parser.errors.mismatch_columns_and_offsets_error import MismatchColumnsAndOffsetsError

REQUIRED_SPECS = ['Offsets', 'FixedWidthEncoding', 'DelimitedEncoding']

def read_spec(spec_file: str) -> Spec:

    with open(spec_file, 'r') as jsonfile:
        spec = json.load(jsonfile)

        if not set(REQUIRED_SPECS).issubset(set(spec)):
            raise MissingSpecError('Spec requires `Offsets`, `FixedWidthEncoding` and `DelimitedEncoding`!')

        if len(spec['ColumnNames']) != len(spec['Offsets']):
            raise MismatchColumnsAndOffsetsError('Columns should match with Offsets!')

        offsets = [int(offset) for offset in spec['Offsets']]
        return Spec(spec['FixedWidthEncoding'], offsets, sum(offsets), spec['DelimitedEncoding'])

def read_content(input_file: str, encoding: str) -> str:

    with open(input_file, 'r', newline="", encoding=encoding) as file:
        return file.read()
