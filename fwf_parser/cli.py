import click

from fwf_parser.parser import run

@click.command()
@click.option("--input-file", required=True, help="Input fixed width file.")
@click.option("--spec-file", required=True, help="Spec file.")

def parse(input_file, spec_file):
    run(input_file, spec_file)

if __name__ == "__main__":
    parse()  # pylint: disable=no-value-for-parameter
