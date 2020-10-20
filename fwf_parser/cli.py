import click

from fwf_parser.parser import read_rows
from fwf_parser.reader import read_spec, read_content
from fwf_parser.writer import write_csv

@click.command()
@click.option("--input-file", required=True, help="Input fixed width file.")
@click.option("--spec-file", required=True, help="Spec file.")
def parse(input_file: str, spec_file: str) ->  None:
    run(input_file, spec_file)

def run(input_file: str, spec_file: str) -> None:
    spec = read_spec(spec_file)
    content = read_content(input_file, spec.input_encoding)

    write_csv(
        read_rows(content, spec.line_width, spec.offsets),
        input_file.replace('.txt', '.csv'),
        spec.output_encoding)

if __name__ == "__main__":
    parse()  # pylint: disable=no-value-for-parameter
