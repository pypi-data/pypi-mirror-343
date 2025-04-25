import json
import tempfile
import typer
from rich.console import Console
from paxpar.cli.tools import call
import sys
import yaml
import toml


console = Console()

app = typer.Typer(help="pp tools / external commands")


@app.command()
def check():
    '''
    Check installed commands (NOT IMPLEMENTED)
    '''
    ...


@app.command()
def install():
    """
    Check installed commands (NOT IMPLEMENTED)
    """
    ...

