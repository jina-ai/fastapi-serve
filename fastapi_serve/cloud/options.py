import click
from jcloud.constants import Phase

from fastapi_serve.cloud.config import (
    APP_NAME,
    DEFAULT_TIMEOUT,
    validate_jcloud_config_callback,
)

_help_option = [click.help_option('-h', '--help')]

_common_options = [
    click.argument(
        'app',
        type=str,
        required=True,
    ),
    click.option(
        '--app-dir',
        type=str,
        required=False,
        help='Base directory to be used for the FastAPI app.',
    ),
]

_hubble_only_options = [
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
]

_hubble_common_options = [
    click.option(
        '--platform',
        type=str,
        required=False,
        help='Platform of Docker image needed for the deployment is built on.',
    ),
    click.option(
        '--version',
        type=str,
        default='latest',
        help='Version of fastapi-serve to be used.',
        show_default=False,
    ),
    click.option(
        '--public',
        is_flag=True,
        help='Push the image publicly.',
        default=False,
        show_default=True,
    ),
    click.option(
        '-v',
        '--verbose',
        is_flag=True,
        help='Verbose mode.',
        show_default=True,
    ),
]

_jcloud_only_options = [
    click.option(
        '--name',
        type=str,
        default=APP_NAME,
        help='Name of the app.',
        show_default=True,
    ),
    click.option(
        '--uses',
        type=str,
        default=None,
        help='Pass a pre-existing image that was pushed using `push-only` option.',
    ),
    click.option(
        '--app-id',
        type=str,
        default=None,
        help='AppID of the deployed app to be updated.',
    ),
    click.option(
        '--timeout',
        type=int,
        default=DEFAULT_TIMEOUT,
        help='Total request timeout in seconds.',
        show_default=True,
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
        '--envs',
        type=click.Path(exists=True),
        help='Path to the environment file (should be a .env file)',
        show_default=False,
    ),
    click.option(
        '--secret',
        '--secrets',
        type=click.Path(exists=True),
        help='Path to the secrets file (should be a .env file)',
        show_default=False,
    ),
    click.option(
        '--cors',
        is_flag=True,
        help='Enable CORS.',
        default=True,
        show_default=True,
    ),
]

_jcloud_list_options = [
    click.option(
        '--phase',
        type=str,
        default=','.join(
            [
                Phase.Serving,
                Phase.Failed,
                Phase.Starting,
                Phase.Updating,
                Phase.Paused,
            ]
        ),
        help='Deployment phase for the app.',
        show_default=True,
    ),
    click.option(
        '--name',
        type=str,
        default=None,
        help='Name of the app.',
        show_default=True,
    ),
]


__all__ = [
    'hubble_push_options',
    'jcloud_deploy_options',
    'jcloud_list_options',
]


def hubble_push_options(func):
    for option in reversed(
        _common_options + _hubble_only_options + _hubble_common_options + _help_option
    ):
        func = option(func)
    return func


def jcloud_deploy_options(func):
    for option in reversed(
        _common_options + _jcloud_only_options + _hubble_common_options + _help_option
    ):
        func = option(func)
    return func


def jcloud_list_options(func):
    for option in reversed(_jcloud_list_options + _help_option):
        func = option(func)
    return func
