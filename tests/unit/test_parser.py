import pytest

from fwf_parser.parser import read_columns


class TestParser:

    @pytest.fixture
    def row_and_offsets(self):
        offsets = ["4", "4", "5", "7"]

        return ("a aa b b  1 c  d  dd\n", offsets)

    def test_read_columns_given_a_row_and_offsets_reads_columns(self,
                                                                row_and_offsets):
        columns = read_columns(*row_and_offsets)

        assert list(columns) == ["a aa", " b b", "  1 c", "  d  dd"]
