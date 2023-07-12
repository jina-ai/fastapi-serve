import click

from fastapi_serve.cloud import (
    get_jinaai_uri,
    hubble_shared_options,
    jcloud_shared_options,
)

from . import __version__


@click.group()
@click.version_option(__version__, "-v", "--version", prog_name="fastapi-serve")
@click.help_option("-h", "--help")
def serve():
    """FastAPI Serve"""
    pass


@serve.command(help="Push the app image to Jina AI Cloud")
@click.argument(
    'app',
    type=str,
    required=True,
)
@click.option(
    '--app-dir',
    type=str,
    required=False,
    help='Base directory to be used for the FastAPI app.',
)
@hubble_shared_options
@click.help_option("-h", "--help")
def push(
    app,
    app_dir,
    image_name,
    image_tag,
    platform,
    requirements,
    version,
    verbose,
    public,
):
    from fastapi_serve.cloud import push_app_to_hubble

    gateway_id = push_app_to_hubble(
        app=app,
        app_dir=app_dir,
        image_name=image_name,
        tag=image_tag,
        platform=platform,
        requirements=requirements,
        version=version,
        verbose=verbose,
        public=public,
    )
    _id, _tag = gateway_id.split(':')
    _uri = click.style(get_jinaai_uri(_id, _tag), fg="green")
    click.echo(f'Pushed to Jina AI Cloud. Please use {_uri} to deploy.')


if __name__ == "__main__":
    serve()
