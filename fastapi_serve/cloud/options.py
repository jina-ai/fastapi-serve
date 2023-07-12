import click

from fastapi_serve.cloud.config import DEFAULT_TIMEOUT, validate_jcloud_config_callback

_hubble_push_options = [
    click.option(
        '--image-name',
        type=str,
        required=False,
        help='Name of the image to be pushed.',
    ),
    click.option(
        '--image-tag',
        type=str,
        default='latest',
        required=False,
        help='Tag of the image to be pushed.',
    ),
    click.option(
        '--platform',
        type=str,
        required=False,
        help='Platform of Docker image needed for the deployment is built on.',
    ),
    click.option(
        '--requirements',
        default=None,
        type=str,
        help='''Pass either

            1) multiple requirements or,
            2) a path to a requirements.txt/pyproject.toml file or,
            3) a directory containing requirements.txt/pyproject.toml file.''',
        multiple=True,
    ),
    click.option(
        '--version',
        type=str,
        default='latest',
        help='Version of serving gateway to be used.',
        show_default=False,
    ),
    click.option(
        '--verbose',
        is_flag=True,
        help='Verbose mode.',
        show_default=True,
    ),
    click.option(
        '--public',
        is_flag=True,
        help='Push the image publicly.',
        default=False,
        show_default=True,
    ),
]


_jcloud_shared_options = [
    click.option(
        '--app-id',
        type=str,
        default=None,
        help='AppID of the deployed agent to be updated.',
        show_default=True,
    ),
    click.option(
        '--requirements',
        default=None,
        type=str,
        help='''Pass either 
        1) multiple requirements or,
        2) a path to a requirements.txt/pyproject.toml file or,
        3) a directory containing requirements.txt/pyproject.toml file.''',
        multiple=True,
    ),
    click.option(
        '--version',
        type=str,
        default='latest',
        help='Version of serving gateway to be used.',
        show_default=False,
    ),
    click.option(
        '--timeout',
        type=int,
        default=DEFAULT_TIMEOUT,
        help='Total request timeout in seconds.',
        show_default=True,
    ),
    click.option(
        '--platform',
        type=str,
        default=None,
        help='Platform of Docker image needed for the deployment is built on.',
        show_default=False,
    ),
    click.option(
        '--config',
        type=click.Path(exists=True),
        help='Path to the config file',
        callback=validate_jcloud_config_callback,
        show_default=False,
    ),
    click.option(
        '--env',
        type=click.Path(exists=True),
        help='Path to the environment file',
        show_default=False,
    ),
    click.option(
        '--cors',
        is_flag=True,
        help='Enable CORS.',
        default=True,
        show_default=True,
    ),
    click.option(
        '--verbose',
        is_flag=True,
        help='Verbose mode.',
        show_default=True,
    ),
    click.option(
        '--public',
        is_flag=True,
        help='Push the image publicly.',
        default=False,
        show_default=True,
    ),
]


def hubble_shared_options(func):
    for option in reversed(_hubble_push_options):
        func = option(func)
    return func


def jcloud_shared_options(func):
    for option in reversed(_jcloud_shared_options):
        func = option(func)
    return func
