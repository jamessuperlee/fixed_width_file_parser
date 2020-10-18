
def read_columns(row, offsets):
    offset, *next_offsets = offsets
    column, rest = row[0:int(offset)], row[int(offset):]

    yield column

    if next_offsets:
        yield from read_columns(rest, next_offsets)
