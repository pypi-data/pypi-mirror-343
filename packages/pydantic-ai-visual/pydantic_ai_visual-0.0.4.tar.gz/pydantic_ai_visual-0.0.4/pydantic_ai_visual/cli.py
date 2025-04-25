import click

from .app import app


@click.command()
@click.option("--host", type=click.STRING, default="0.0.0.0")  # noqa: S104
@click.option("--port", type=click.INT, default=8891)
def start(host, port):
    """
    Start the server.
    """
    app.launch(server_port=port, server_name=host, share=True)


@click.group()
def cli():
    pass


cli.add_command(start)
