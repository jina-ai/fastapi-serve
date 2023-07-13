import click

from fastapi_serve import __version__
from fastapi_serve.cloud import (
    get_app_status_on_jcloud,
    get_jinaai_uri,
    hubble_push_options,
    jcloud_deploy_options,
    jcloud_list_options,
    list_apps_on_jcloud,
    push_app_to_hubble,
    remove_app_on_jcloud,
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
@hubble_push_options
@click.help_option("-h", "--help")
def push(app, app_dir, image_name, image_tag, platform, version, verbose, public):
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


@serve.group(help="Deploy the app.")
@click.help_option("-h", "--help")
def deploy():
    pass


@deploy.command(help="Deploy the app locally")
@click.help_option("-h", "--help")
@syncify
async def local():
    pass


@deploy.command(help="Deploy the app to Jina AI Cloud")
@jcloud_deploy_options
@syncify
async def jcloud(
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
    secret,
    verbose,
    public,
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
        secret=secret,
        verbose=verbose,
        public=public,
    )


@serve.command(help='List all deployed apps.')
@jcloud_list_options
@syncify
async def list(phase, name):
    await list_apps_on_jcloud(phase=phase, name=name)


@serve.command(help='Get status of a deployed app.')
@click.argument('app-id')
@click.help_option('-h', '--help')
@syncify
async def status(app_id):
    await get_app_status_on_jcloud(app_id)


@serve.command(help='Remove an app.')
@click.argument('app-id')
@click.help_option('-h', '--help')
@syncify
async def remove(app_id):
    await remove_app_on_jcloud(app_id)


if __name__ == "__main__":
    serve()
