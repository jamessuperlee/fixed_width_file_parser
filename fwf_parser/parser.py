import csv
import json

from fwf_parser.errors.row_width_mismatch_error import RowWidthMismatchError
from fwf_parser.reader import read_spec

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

    with open(input_file, 'r', encoding=spec['input_encoding'], newline='') as fwfile:
        content = fwfile.read()

    output_file = input_file.replace('.txt', '.csv')

    with open(output_file, 'w', encoding=spec['output_encoding'], newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(read_rows(content, spec['line_width'], spec['offsets']))
