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


    @pytest.fixture
    def all_characters_content_and_spec_and_expected_rows(self):
        spec = {
            "ColumnNames": [
                "a",
                "b",
                "c",
                "d"
            ],
            "Offsets": [
                "10",
                "5",
                "5",
                "5"
            ],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8"
        }

        def generate_bytes_chars(row_characters, offsets):
            offset, *rest_offsets = offsets
            column_characters, rest_characters = row_characters[:int(offset)], row_characters[int(offset):]
            yield ''.join(column_characters)

            if rest_characters:
                yield from generate_bytes_chars(rest_characters, rest_offsets)

        def generate_content(charaters, offsets):
            row_characters, rest = charaters[:25], charaters[25:]

            yield generate_bytes_chars(row_characters, offsets), ''.join(row_characters)

            if rest:
                yield from generate_content(rest, offsets)

        # windows-1252 encoding is single byte character.
        # The range of characters is from 0x00 to 0xFF.
        # But windows-1252 encoding does not support 5 codes - 0x81, 0x8d, 0x8f, 0x90, 0x9d
        # NUL(0x00) is excluded because csv reader cannot read it.
        all_possible_charaters = [
            bytes([i]).decode('windows-1252')
            for i in range(256)[1:] if not i in [129, 141, 143, 144, 157]]

        expected_rows, rows = zip(*[
            (list(row_characters), content)
            for row_characters, content in generate_content(all_possible_charaters, spec['Offsets'])])

        header = ["         a", "    b", "    c", "    d"]

        content = '\n'.join([''.join(header), *rows])

        return content, spec, [header, *expected_rows]

    @pytest.fixture
    def file_with_all_characters_and_spec_file(self, all_characters_content_and_spec_and_expected_rows):
        content, spec, expected_rows = all_characters_content_and_spec_and_expected_rows

        spec_filepath = './test-spec.json'
        with open(spec_filepath, 'w') as jsonfile:
            json.dump(spec, jsonfile)

        input_filepath = './test-fixed-width-file.txt'
        with open(input_filepath, 'w', encoding=spec['FixedWidthEncoding']) as file:
            file.write(content)

        yield input_filepath, spec_filepath, expected_rows

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


    def test_run_given_a_file_with_all_characters_generates_a_valid_csv(self,
                                                                        file_with_all_characters_and_spec_file):
        input_filepath, spec_filepath, expected_rows = file_with_all_characters_and_spec_file

        run(input_filepath, spec_filepath)

        with open(input_filepath.replace('.txt', '.csv'), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        assert rows == expected_rows
