import typer
from rich.console import Console
from paxpar.cli.tools import call


console = Console()

app = typer.Typer(help="Python related pp commands")




@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def core(ctx: typer.Context):
    """
    Run python from paxpar core service env
    """
    extra_args = " ".join(list(ctx.args))
    call(
        f"""
        ./services/core/.venv/bin/python -m asyncio {extra_args}
    """
    )


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def perm(ctx: typer.Context):
    """
    Run python from paxpar perm service env
    """
    extra_args = " ".join(list(ctx.args))
    call(
        f"""
        ./services/core/.venv/bin/python -m asyncio {extra_args}
    """
    )


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def auth(ctx: typer.Context):
    """
    Run python from paxpar auth service env
    """
    extra_args = " ".join(list(ctx.args))
    call(
        f"""
        ./services/core/.venv/bin/python -m asyncio {extra_args}
    """
    )



@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def jlab(ctx: typer.Context):
    """
    Run jlab desktop jupyter from paxpar core service env
    """
    extra_args = " ".join(list(ctx.args)) if len(ctx.args) > 0 else "."
    call(
        f"""
        jlab {extra_args}
    """
    )
