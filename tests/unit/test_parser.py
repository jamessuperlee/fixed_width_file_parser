import pytest

from fwf_parser.parser import read_columns, read_rows
from fwf_parser.row_width_mismatch_error import RowWidthMismatchError


class TestParser:

    @pytest.fixture
    def row_and_offsets(self):
        offsets = ["4", "4", "5", "7"]

        return ("a aa b b  1 c  d  dd\n", offsets)

    @pytest.fixture
    def file_content_and_offsets(self):
        return '''\
 col1        col2 col3
   aa       bbbbb   cc
aa aa       cc  c    d
  ttt          ss   zz
    a           c    i
kkkkk     ddd   d d  c
''', ["5", "12", "5"]

    @pytest.fixture
    def file_content_with_a_short_row_and_offsets(self):
        return '''\
 col1        col2 col3
   aa       bbbbb   cc
aa aa       b
  ttt          ss   zz
    a           c    i
kkkkk     ddd   d d  c
''', ["5", "12", "5"]


    def test_read_columns_given_a_row_and_offsets_reads_columns(self,
                                                                row_and_offsets):
        columns = read_columns(*row_and_offsets)

        assert list(columns) == ["a aa", " b b", "  1 c", "  d  dd"]

    def test_read_rows_given_a_file_content_and_offsets_reads_all_rows(self,
                                                                       file_content_and_offsets):
        content, offsets = file_content_and_offsets
        line_width = sum([int(offset) for offset in offsets])

        rows = read_rows(content, line_width, offsets)

        expected_rows = [
            [" col1","        col2"," col3"],
            ["   aa","       bbbbb","   cc"],
            ["aa aa","       cc  c","    d"],
            ["  ttt","          ss","   zz"],
            ["    a","           c","    i"],
            ["kkkkk","     ddd   d"," d  c"]
        ]

        assert [list(row) for row in rows] == expected_rows

    def test_read_rows_given_content_with_a_short_row_raises_an_error(self,
                                                                      file_content_with_a_short_row_and_offsets):

        content, offsets = file_content_with_a_short_row_and_offsets

        with pytest.raises(RowWidthMismatchError, match="Row width does not match with spec offset!"):
            rows = read_rows(
                content,
                sum([int(offset) for offset in offsets]),
                offsets)
            list(rows)
