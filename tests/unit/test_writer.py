from unittest.mock import Mock, patch, mock_open

import pytest

from fwf_parser.writer import write_csv


class TestWriter:
    @pytest.fixture
    def rows(self):
        return [
            ["col1", "col2"],
            ["  ab", " ccc"]
        ]

    @patch('fwf_parser.writer.csv')
    @patch('builtins.open', new_callable=mock_open())
    def test_write_csv_given_valid_rows_generates_a_csv_file(self, mock_file, mock_csv, rows):
        mock_csv.writer = Mock(writerows=Mock())

        output_file = './test.csv'
        encoding = 'utf-8'

        write_csv(rows, output_file, encoding)

        mock_file.assert_called_once_with(output_file, 'w', newline="", encoding=encoding)
        mock_csv.writer.assert_called_once()
        mock_csv.writer().writerows.assert_called_once_with(rows)
