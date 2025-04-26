import typer
from pathlib import Path

from cyberfusion.FoundryAgent.config import Config
from cyberfusion.FoundryAgent.modules.heartbeats import HeartbeatModule

app = typer.Typer()


@app.command()  # type: ignore[misc]
def send_heartbeat(
    config_file_path: Path = typer.Option(
        ...,
        "--config-file-path",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
) -> None:
    config = Config(config_file_path)

    module = HeartbeatModule(config)
    module.run()

    typer.secho("Heartbeat sent", fg=typer.colors.GREEN)


@app.callback()  # type: ignore[misc]
def callback() -> None:
    """Workaround (https://typer.tiangolo.com/tutorial/commands/one-or-multiple/#one-command-and-one-callback)"""
    pass
