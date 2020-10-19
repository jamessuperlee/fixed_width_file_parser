import json
from unittest.mock import patch, mock_open

import pytest

from fwf_parser.reader import read_spec
from fwf_parser.errors.invalid_spec_error import InvalidSpecError


class TestReader:

    @pytest.fixture
    def spec(self):
        return {
            "ColumnNames": [
                "col1"
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


    def test_read_spec_given_invalid_spec_raises_an_valid_spec_error(self, invalid_spec):
        with patch('builtins.open', mock_open(read_data=json.dumps(invalid_spec))):
            spec_file = "./spec.json"

            with pytest.raises(
                InvalidSpecError,
                match="Spec requires `Offsets`, `FixedWidthEncoding` and `DelimitedEncoding`!"):
                read_spec(spec_file)
