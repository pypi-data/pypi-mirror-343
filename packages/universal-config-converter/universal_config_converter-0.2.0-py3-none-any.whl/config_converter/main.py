import click
from .converter import convert
import sys  # Import sys for exit codes


@click.command()
@click.option(
    "--input-file",
    "-i",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the input configuration file.",
)
@click.option(
    "--source-format",
    "-s",
    required=True,
    type=click.Choice(
        ["json", "yaml", "toml", "env", "ini", "xml"], case_sensitive=False
    ),
    help="Format of the input file.",
)
@click.option(
    "--target-format",
    "-t",
    required=True,
    type=click.Choice(
        ["json", "yaml", "toml", "env", "ini", "xml"], case_sensitive=False
    ),
    help="Format for the output file.",
)
@click.option(
    "--output-file",
    "-o",
    required=True,
    type=click.Path(dir_okay=False),
    help="Path to save the converted configuration file.",
)
@click.option(
    "--input-schema",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to a JSON schema file to validate the input against.",
)
@click.option(
    "--output-schema",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to a JSON schema file to validate the output against.",
)
def main(
    input_file, source_format, target_format, output_file, input_schema, output_schema
):
    """Universal Config Converter CLI"""
    try:
        convert(
            input_file,
            source_format,
            target_format,
            output_file,
            input_schema,
            output_schema,
        )
        click.echo(
            f"Successfully converted '{input_file}' ({source_format}) to "
            f"'{output_file}' ({target_format})"
        )
    except ValueError as e:  # Catch specific errors like validation errors
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)  # Exit with non-zero status for errors
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
