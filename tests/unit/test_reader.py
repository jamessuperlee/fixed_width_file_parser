import json
from unittest.mock import patch, mock_open

import pytest

from fwf_parser.reader import read_spec, read_content
from fwf_parser.errors.missing_spec_error import MissingSpecError
from fwf_parser.errors.mismatch_columns_and_offsets_error import MismatchColumnsAndOffsetsError


class TestReader:

    @pytest.fixture
    def spec(self):
        return {
            "ColumnNames": [
                "col1",
                "col2"
            ],
            "Offsets": [
                "3",
                "5"
            ],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8"
        }

    @pytest.fixture
    def invalid_spec(self):
        return {
            "ColumnNames": [
                "col1"
            ],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8"
        }

    @pytest.fixture
    def mismatch_columns_and_offsets(self):
        return {
            "ColumnNames": [
                "col1"
            ],
            "Offsets": [
                "1",
                "2"
            ],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8"
        }

    @pytest.fixture
    def content(self):
        return '''\
col1 col2 col5
   a    b    c
'''

    def test_read_spec_given_valid_spec_return_spec_dict(self, spec):
        with patch('builtins.open', mock_open(read_data=json.dumps(spec))) as mock_file:
            spec_file = "./spec.json"

            expected_spec = {
                "input_encoding": "windows-1252",
                "offsets": [3, 5],
                "line_width": 8,
                "output_encoding": "utf-8"
            }

            assert read_spec(spec_file) == expected_spec
            mock_file.assert_called_with(spec_file, 'r')

    def test_read_input_file_given_valid_input_file_returns_content(self, content):
        with patch('builtins.open', mock_open(read_data=content)) as mock_file:
            input_file = "./fwf.txt"

            assert read_content(input_file, 'windows-1252') == content
            mock_file.assert_called_with(input_file, 'r', newline="", encoding='windows-1252')

    def test_read_spec_given_invalid_spec_raises_an_error(self, invalid_spec):
        with patch('builtins.open', mock_open(read_data=json.dumps(invalid_spec))):
            spec_file = "./spec.json"

            with pytest.raises(
                MissingSpecError,
                match="Spec requires `Offsets`, `FixedWidthEncoding` and `DelimitedEncoding`!"):
                read_spec(spec_file)

    def test_read_spec_given_mismatch_columns_and_offsets_raises_an_error(self, mismatch_columns_and_offsets):
        with patch('builtins.open', mock_open(read_data=json.dumps(mismatch_columns_and_offsets))):
            spec_file = "./spec.json"

            with pytest.raises(
                MismatchColumnsAndOffsetsError,
                match="Columns should match with Offsets!"):
                read_spec(spec_file)
