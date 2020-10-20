
from fwf_parser.errors.row_width_mismatch_error import RowWidthMismatchError


def strip_padding(chars):
    char, next_chars = chars[:1], chars[1:]

    if char != ' ':
        return chars

    return strip_padding(next_chars)


def read_columns(row, offsets):
    offset, *next_offsets = offsets
    column, rest = row[0:offset], row[offset:]

    yield strip_padding(column)

    if next_offsets:
        yield from read_columns(rest, next_offsets)

def read_rows(content, row_width, offsets):
    row, rest_content = content[0:row_width], content[row_width + 1:]

    if len(row) != row_width:
        raise RowWidthMismatchError('Row width does not match with spec offset!')

    yield read_columns(row, offsets)

    if rest_content:
        yield from read_rows(rest_content, row_width, offsets)
