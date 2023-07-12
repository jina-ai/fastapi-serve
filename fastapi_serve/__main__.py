import click

from fastapi_serve import __version__
from fastapi_serve.cloud import (
    get_jinaai_uri,
    hubble_options,
    jcloud_options,
    push_app_to_hubble,
    serve_on_jcloud,
)
from fastapi_serve.helper import syncify


@click.group()
@click.version_option(__version__, "-v", "--version", prog_name="fastapi-serve")
@click.help_option("-h", "--help")
def serve():
    """FastAPI Serve - FastAPI to the Cloud, Batteries Included! ☁️🔋🚀"""
    pass


@serve.command(help="Push the app image to Jina AI Cloud")
@hubble_options
@click.help_option("-h", "--help")
def push(
    app,
    app_dir,
    image_name,
    image_tag,
    platform,
    version,
    verbose,
    public,
):
    _gateway_id = push_app_to_hubble(
        app=app,
        app_dir=app_dir,
        image_name=image_name,
        tag=image_tag,
        platform=platform,
        version=version,
        verbose=verbose,
        public=public,
    )
    _id, _tag = _gateway_id.split(':')
    _uri = click.style(get_jinaai_uri(_id, _tag), fg="green")
    click.echo(f'Pushed to Jina AI Cloud. Please use {_uri} to deploy.')


@serve.command(help="Deploy the app image to Jina AI Cloud")
@jcloud_options
@click.help_option("-h", "--help")
@syncify
async def deploy(
    app,
    app_dir,
    name,
    uses,
    app_id,
    version,
    timeout,
    platform,
    config,
    cors,
    env,
    verbose,
    public,
    secret,
):
    await serve_on_jcloud(
        app=app,
        app_dir=app_dir,
        name=name,
        uses=uses,
        app_id=app_id,
        version=version,
        timeout=timeout,
        platform=platform,
        config=config,
        cors=cors,
        env=env,
        verbose=verbose,
        public=public,
        secret=secret,
    )


if __name__ == "__main__":
    serve()
