# cthulhucrypt/cli.py
import click
from .core import (
    super_encrypt,
    character_pairing,
    bitwise_xor_transform,
    math_chaos,
    dynamic_substitute,
    ultra_encrypt
)

@click.group()
def cli():
    """CthulhuCrypt CLI - An unholy encryption toolkit."""
    pass

@cli.command()
@click.argument("text")
def super_encrypt_cli(text):
    """Run super_encrypt on text."""
    result = super_encrypt(text)
    click.echo(f"Super Encrypted: {result}")

@cli.command()
@click.argument("text")
def character_pairing_cli(text):
    """Run character_pairing on text."""
    result = character_pairing(text)
    click.echo(f"Paired Digits: {result}")

@cli.command()
@click.argument("text")
def xor_transform_cli(text):
    """Run bitwise_xor_transform on text."""
    result = bitwise_xor_transform(text)
    click.echo(f"XOR Transformed: {result}")

@cli.command()
@click.argument("text")
def math_chaos_cli(text):
    """Run math_chaos on text."""
    result = math_chaos(text)
    click.echo(f"Math Chaos: {result}")

@cli.command()
@click.argument("text")
@click.option("--table-id", default=0, help="Table index for substitution")
def substitute_cli(text, table_id):
    """Run dynamic_substitute on text."""
    from .core import TABLES
    result = dynamic_substitute(text, [TABLES[table_id]])  # Single table for CLI
    click.echo(f"Substituted: {result}")

@cli.command()
@click.argument("text")
@click.option("--iterations", default=7, help="Ultra encryption passes")
def ultra_encrypt_cli(text, iterations):
    """Run ultra_encrypt on text."""
    result = ultra_encrypt(text, iterations)
    click.echo(f"Ultra Encrypted: {result}")

if __name__ == "__main__":
    cli()