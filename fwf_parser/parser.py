import csv
import json

from fwf_parser.row_width_mismatch_error import RowWidthMismatchError


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
    with open(spec_file, 'r') as jsonfile:
        spec = json.load(jsonfile)

    with open(input_file, 'r', encoding=spec['FixedWidthEncoding'], newline='') as fwfile:
        content = fwfile.read()

    output_file = input_file.replace('.txt', '.csv')

    line_width = sum([int(offset) for offset in spec['Offsets']])

    with open(output_file, 'w', encoding=spec['DelimitedEncoding'], newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(read_rows(content, line_width, spec['Offsets']))
