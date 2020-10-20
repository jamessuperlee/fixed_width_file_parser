import pytest

from fwf_parser.parser import strip_padding, read_columns, read_rows
from fwf_parser.errors.row_width_mismatch_error import RowWidthMismatchError


class TestParser:

    @pytest.fixture
    def row_and_offsets(self):
        offsets = [4, 4, 5, 7]

        return ("a aa b b 1 c   d  dd\n", offsets)

    @pytest.fixture
    def file_content_and_offsets(self):
        return '''\
 col1        col2 col3
   aa       bbbbb   cc
aa aa       cc  c    d
  ttt          ss   zz
    a           c    i
kkkkk     ddd   d d  c
''', [5, 12, 5]

    @pytest.fixture
    def file_content_with_mismatch_row_width_and_offsets(self):
        return '''\
 col1        col2 col3
   aa       bbbbb   cc
aa aa       b
  ttt          ss   zz
    a           c    i
kkkkk     ddd   d d  c
''', [5, 12, 5]

    @pytest.fixture
    def file_content_with_mismatch_single_row_width_and_offset(self):
        return '''\
 col1
  a
''', [5]

    def test_strip_padding_given_a_string_strips_left_padding(self):
        test_cases_and_results = [
            (" ", ""),
            ("  ", ""),
            ("a ", "a "),
            (" a ","a "),
            ("   a b  ", "a b  ")
        ]
        for chars, expected_chars in test_cases_and_results:
            assert strip_padding(chars) == expected_chars

    def test_strip_padding_given_a_string_with_control_characters_strips_only_space_padding(self):
        chars = bytes([32,8,9,10,11,65,66]).decode('windows-1252')

        assert strip_padding(chars) == "\x08\t\n\x0bAB"

    def test_read_columns_given_a_row_and_offsets_reads_columns(self,
                                                                row_and_offsets):
        columns = read_columns(*row_and_offsets)

        assert list(columns) == ["a aa", "b b", "1 c ", "d  dd"]

    def test_read_rows_given_a_file_content_and_offsets_reads_all_rows(self,
                                                                       file_content_and_offsets):
        content, offsets = file_content_and_offsets
        line_width = sum(offsets)

        rows = read_rows(content, line_width, offsets)

        expected_rows = [
            ["col1","col2","col3"],
            ["aa","bbbbb","cc"],
            ["aa aa","cc  c","d"],
            ["ttt","ss","zz"],
            ["a","c","i"],
            ["kkkkk","ddd   d","d  c"]
        ]

        assert [list(row) for row in rows] == expected_rows

    def test_read_rows_given_content_with_mismatch_row_width_raises_an_error(self,
                                                        file_content_with_mismatch_row_width_and_offsets):

        content, offsets = file_content_with_mismatch_row_width_and_offsets

        with pytest.raises(RowWidthMismatchError, match="Row width does not match with spec offset!"):
            rows = read_rows(
                content,
                sum(offsets),
                offsets)
            list(rows)

    def test_read_rows_given_content_with_mismatch_single_row_width_raises_an_error(self,
                                                        file_content_with_mismatch_single_row_width_and_offset):

        content, offsets = file_content_with_mismatch_single_row_width_and_offset

        with pytest.raises(RowWidthMismatchError, match="Row width does not match with spec offset!"):
            rows = read_rows(
                content,
                sum(offsets),
                offsets)
            list(rows)
