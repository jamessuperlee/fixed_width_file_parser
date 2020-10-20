import csv
from typing import Generator

def write_csv(
    rows: Generator[Generator[str, None, None], None, None],
    output_file:str, encoding: str) -> None:

    with open(output_file, 'w', newline='', encoding=encoding) as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)
