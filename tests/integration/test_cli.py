import csv
import json
import os
from typing import Dict, Generator, List, Sequence, Tuple

import pytest

from fwf_parser.cli import run

def generate_input_and_spec(
    content_and_spec: Tuple[str, Dict[str, Sequence[str]]]) -> Tuple[str, str]:
    content, spec = content_and_spec

    spec_filepath = './test-spec.json'
    with open(spec_filepath, 'w') as jsonfile:
        json.dump(spec, jsonfile)

    input_filepath = './test-fixed-width-file.txt'
    with open(input_filepath, 'w', encoding='windows-1252') as file:
        file.write(content)

    return input_filepath, spec_filepath


class TestCli:

    @pytest.fixture
    def content_with_single_column_and_spec(self) -> Tuple[str, Dict[str, Sequence[str]]]:
        content = '''\
               f1
    ss   ss   ss 
'''
        spec = {
            "ColumnNames": [
                "f1"
            ],
            "Offsets": [
                "17"
            ],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8"
        }
        return content, spec

    @pytest.fixture
    def file_with_single_column_and_spec_file(
    self,
    content_with_single_column_and_spec: Tuple[str, Dict[str, Sequence[str]]])\
        -> Generator[Tuple[str, str], None, None]:
        input_filepath, spec_filepath = \
            generate_input_and_spec(content_with_single_column_and_spec)

        yield input_filepath, spec_filepath

        os.remove(input_filepath)
        os.remove(input_filepath.replace('.txt', '.csv'))
        os.remove(spec_filepath)

    @pytest.fixture
    def content_with_simple_characters_and_spec(self)\
        -> Tuple[str, Dict[str, Sequence[str]]]:
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
    def file_with_simple_characters_and_spec_file(self,
    content_with_simple_characters_and_spec: Tuple[str, Dict[str, Sequence[str]]])\
        -> Generator[Tuple[str, str], None, None]:
        input_filepath, spec_filepath = \
            generate_input_and_spec(content_with_simple_characters_and_spec)

        yield input_filepath, spec_filepath

        os.remove(input_filepath)
        os.remove(input_filepath.replace('.txt', '.csv'))
        os.remove(spec_filepath)


    @pytest.fixture
    def all_characters_content_and_spec_and_expected_rows(self)\
        -> Tuple[str, Dict[str, Sequence[str]], List[List[str]]]:
        spec = {
            "ColumnNames": [
                "a",
                "b",
                "c",
                "d"
            ],
            "Offsets": [
                "12",
                "6",
                "7",
                "7"
            ],
            "FixedWidthEncoding": "windows-1252",
            "IncludeHeader": "True",
            "DelimitedEncoding": "utf-8"
        }

        def generate_bytes_chars(row_characters: List[str], offsets: List[int])\
            -> Generator[str, None, None]:
            offset, *rest_offsets = offsets
            column_characters, rest_characters = \
                row_characters[:int(offset)], row_characters[int(offset):]
            yield ''.join(column_characters)

            if rest_characters:
                yield from generate_bytes_chars(rest_characters, rest_offsets)

        def generate_content(charaters: List[str], offsets: Sequence[str])\
            -> Generator[Tuple[Generator[str, None, None], str], None, None]:
            row_characters, rest = charaters[:25], charaters[25:]
            row_string_with_space_padding = f'''\
  {''.join(row_characters[:10])} {''.join(row_characters[10:15])}  {''.join(row_characters[15:20])}  {''.join(row_characters[20:25])}\
'''

            stripped_padding_offsets = [10, 5, 5, 5]
            yield generate_bytes_chars(row_characters, stripped_padding_offsets), row_string_with_space_padding

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
            for row_characters, content in generate_content(all_possible_charaters, spec['Offsets'])
        ])

        header = ["           a", "     b", "      c", "      d"]

        content = '\n'.join([''.join(header), *rows])

        return content, spec, [["a", "b", "c", "d"], *expected_rows]

    @pytest.fixture
    def file_with_all_characters_and_spec_file(self,
        all_characters_content_and_spec_and_expected_rows: Tuple[str, Dict[str, Sequence[str]], List[List[str]]])\
        -> Generator[Tuple[str, str, List[List[str]]], None, None]:
        content, spec, expected_rows = all_characters_content_and_spec_and_expected_rows

        input_filepath, spec_filepath = generate_input_and_spec((content, spec))

        yield input_filepath, spec_filepath, expected_rows

        os.remove(input_filepath)
        os.remove(input_filepath.replace('.txt', '.csv'))
        os.remove(spec_filepath)


    def test_run_given_a_file_with_single_column_and_spec_file_generates_a_csv_file(
        self,
        file_with_single_column_and_spec_file):
        input_file, spec_file = file_with_single_column_and_spec_file

        run(input_file, spec_file)

        with open(input_file.replace('.txt', '.csv'), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        expected_content = [
            ["f1"],
            ["ss   ss   ss "]
        ]

        assert rows == expected_content

    def test_run_given_a_file_with_simple_content_and_spec_file_generates_a_csv_file(
        self,
        file_with_simple_characters_and_spec_file):

        input_file, spec_file = file_with_simple_characters_and_spec_file

        run(input_file, spec_file)

        with open(input_file.replace('.txt', '.csv'), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        expected_content = [
            ["col1", "col2", "col3"],
            ["aa", "bbbbb", "cc"],
            ["aa aa", "cc  c", "d"],
            ["ttt", "ss", "zz"]
        ]

        assert rows == expected_content

    def test_run_given_a_file_with_all_characters_generates_a_valid_csv(
        self,
        file_with_all_characters_and_spec_file):

        input_filepath, spec_filepath, expected_rows = file_with_all_characters_and_spec_file

        run(input_filepath, spec_filepath)

        with open(input_filepath.replace('.txt', '.csv'), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        assert rows == expected_rows
