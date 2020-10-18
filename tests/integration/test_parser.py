import csv
import json
import os

import pytest

from fwf_parser.parser import run

class TestParser:

    @pytest.fixture
    def content_with_simple_characters_and_spec(self):
        content = '''\
 col1        col2 col3
   aa       bbbbb   cc
aa aa       cc  c    d
  ttt          ss   zz
'''
        spec = {
            "ColumnNames": [
                "col1",
                "col2",
                "col3"
            ],
            "Offsets": [
                "5",
                "12",
                "5"
            ],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8"
        }
        return content, spec

    @pytest.fixture
    def file_with_simple_characters_and_spec_file(self, content_with_simple_characters_and_spec):
        content, spec = content_with_simple_characters_and_spec

        spec_filepath = './test-spec.json'
        with open(spec_filepath, 'w') as jsonfile:
            json.dump(spec, jsonfile)

        input_filepath = './test-fixed-width-file.txt'
        with open(input_filepath, 'w', encoding=spec['FixedWidthEncoding']) as file:
            file.write(content)

        yield input_filepath, spec_filepath

        os.remove(input_filepath)
        os.remove(input_filepath.replace('.txt', '.csv'))
        os.remove(spec_filepath)

    def test_run_given_a_fixed_width_file_and_spec_file_generates_a_csv_file(self,
                                                                             file_with_simple_characters_and_spec_file):
        input_file, spec_file = file_with_simple_characters_and_spec_file

        run(input_file, spec_file)

        with open(input_file.replace('.txt', '.csv'), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        expected_content = [
            [" col1", "        col2", " col3"],
            ["   aa", "       bbbbb", "   cc"],
            ["aa aa", "       cc  c", "    d"],
            ["  ttt", "          ss", "   zz"]
        ]

        assert rows == expected_content
