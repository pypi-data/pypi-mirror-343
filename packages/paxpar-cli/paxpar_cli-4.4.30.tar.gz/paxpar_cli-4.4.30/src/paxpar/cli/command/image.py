import os
import typer
from rich.console import Console

from paxpar.cli.tools import call, root_command_callback

console = Console()

app = typer.Typer(
    help="container image related commands",
    callback=root_command_callback(),
)


REGISTRIES = {
    "gitea": {
        "url": "gitea.arundo.tech",
    },
    "gitlab": {
        "url": "registry.gitlab.com",
    },
    "scaleway": {
        "url": "rg.fr-par.scw.cloud/pp-registry-test1",
    },
}


@app.command("list")
def list_command():
    """
    List image registries
    """
    print(REGISTRIES)


@app.command()
def login(
    ctx: typer.Context,
    registry_id: str = "all",
):
    """
    Login to image registry
    """
    registries = list(REGISTRIES.keys()) if registry_id == "all" else [registry_id]

    for registry_id in registries:
        registry = REGISTRIES[registry_id]
        envv = f"{registry_id.upper()}_SECRET_KEY"
        secret = os.environ[envv]
        cmd = f'''podman login {registry["url"]} -u nologin -p "{secret}"'''

        call(cmd, ctx_obj=ctx.obj)


@app.command()
def pull(
    ctx: typer.Context,
    version: str = "latest",
):
    """
    Pull paxpar core image
    """
    registry = REGISTRIES["gitlab"]
    if version[0].isdigit():
        version = f"v{version}"

    call(
        f"""podman pull {registry["url"]}/arundo-tech/paxpar/paxpar-core:{version}""",
        ctx_obj=ctx.obj,
    )


@app.command()
def run(
    ctx: typer.Context,
):
    """
    Run default python image
    """

    call(
        """
        podman run \
            -t -i --rm \
            -v $PWD:/builds/arundo-tech/paxpar \
            -w /builds/arundo-tech/paxpar \
            --entrypoint /bin/bash \
            python:3.13
        """,
        ctx_obj=ctx.obj,
    )
