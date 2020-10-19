
from fwf_parser.errors.row_width_mismatch_error import RowWidthMismatchError
from fwf_parser.reader import read_spec, read_content
from fwf_parser.writer import write_csv


def read_columns(row, offsets):
    offset, *next_offsets = offsets
    column, rest = row[0:int(offset)], row[int(offset):]

    yield column

    if next_offsets:
        yield from read_columns(rest, next_offsets)

def read_rows(content, row_width, offsets):
    row, rest_content = content[0:row_width], content[row_width + 1:]

    if len(row) != row_width:
        raise RowWidthMismatchError('Row width does not match with spec offset!')

    yield read_columns(row, offsets)

    if rest_content:
        yield from read_rows(rest_content, row_width, offsets)

def run(input_file, spec_file):
    spec = read_spec(spec_file)
    content = read_content(input_file, spec['input_encoding'])

    write_csv(
        read_rows(content, spec['line_width'], spec['offsets']),
        input_file.replace('.txt', '.csv'),
        spec['output_encoding'])
