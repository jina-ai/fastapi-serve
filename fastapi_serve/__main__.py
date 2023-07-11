import click

from . import __version__


@click.group()
@click.version_option(__version__, "-v", "--version", prog_name="fastapi-serve")
@click.help_option("-h", "--help")
def serve():
    """FastAPI Serve"""
    pass


if __name__ == "__main__":
    serve()
