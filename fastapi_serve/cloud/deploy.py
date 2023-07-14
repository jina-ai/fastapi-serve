import os
from tempfile import TemporaryDirectory
from typing import Dict, List, Tuple

import yaml
from dotenv import dotenv_values

from fastapi_serve.cloud.config import (
    APP_LOGS_URL,
    APP_NAME,
    DEFAULT_LABEL,
    DEFAULT_TIMEOUT,
    DOCARRAY_VERSION,
    JINA_VERSION,
    PRICING_URL,
    get_jcloud_config,
)
from fastapi_serve.helper import (
    EnvironmentVarCtxtManager,
    asyncio_run_property,
    get_random_name,
)


def get_gateway_config_yaml_path() -> str:
    return os.path.join(os.path.dirname(__file__), 'config.yml')


def get_gateway_uses(id: str) -> str:
    if id is not None:
        if id.startswith('jinahub+docker') or id.startswith('jinaai+docker'):
            return id
    return f'jinahub+docker://{id}'


def get_existing_name(app_id: str) -> str:
    from jcloud.flow import CloudFlow

    flow_obj = asyncio_run_property(CloudFlow(flow_id=app_id).status)
    if (
        'spec' in flow_obj
        and 'jcloud' in flow_obj['spec']
        and 'name' in flow_obj['spec']['jcloud']
    ):
        return flow_obj['spec']['jcloud']['name']


def get_global_jcloud_args(app_id: str = None, name: str = APP_NAME) -> Dict:
    if app_id is not None:
        _name = get_existing_name(app_id)
        if _name is not None:
            name = _name

    return {
        'jcloud': {
            'name': name,
            'labels': {
                'app': DEFAULT_LABEL,
            },
            'version': JINA_VERSION,
            'docarray': DOCARRAY_VERSION,
            'monitor': {
                'traces': {
                    'enable': True,
                },
                'metrics': {
                    'enable': True,
                    'host': 'http://opentelemetry-collector.monitor.svc.cluster.local',
                    'port': 4317,
                },
            },
        }
    }


def get_uvicorn_args() -> Dict:
    return {
        'uvicorn_kwargs': {
            'ws_ping_interval': None,
            'ws_ping_timeout': None,
        }
    }


def get_with_args_for_jcloud(cors: bool = True, envs: Dict = {}) -> Dict:
    return {
        'with': {
            'cors': cors,
            'extra_search_paths': ['/workdir/fastapi_serve'],
            'env': envs or {},
            **get_uvicorn_args(),
        }
    }


def get_flow_dict(
    app: str,
    jcloud: bool = False,
    port: int = 8080,
    name: str = APP_NAME,
    timeout: int = DEFAULT_TIMEOUT,
    app_id: str = None,
    gateway_id: str = None,
    is_websocket: bool = False,
    jcloud_config_path: str = None,
    cors: bool = True,
    env: str = None,
) -> Dict:
    if jcloud:
        jcloud_config = get_jcloud_config(
            config_path=jcloud_config_path, timeout=timeout, is_websocket=is_websocket
        )

    _envs = {}
    if env is not None:
        # read env file and load to _envs dict
        _envs = dict(dotenv_values(env))

    uses = get_gateway_uses(id=gateway_id) if jcloud else get_gateway_config_yaml_path()
    flow_dict = {
        'jtype': 'Flow',
        **(get_with_args_for_jcloud(cors, _envs) if jcloud else {}),
        'gateway': {
            'uses': uses,
            'uses_with': {
                'app': app,
            },
            'port': [port],
            'protocol': ['websocket'] if is_websocket else ['http'],
            'env': _envs if _envs else {},
            **get_uvicorn_args(),
            **(jcloud_config.to_dict() if jcloud else {}),
        },
        **(get_global_jcloud_args(app_id=app_id, name=name) if jcloud else {}),
    }
    if os.environ.get("FASTAPI_SERVE_TEST", False):
        if 'with' not in flow_dict:
            flow_dict['with'] = {}

        flow_dict['with'].update(
            {
                'metrics': True,
                'metrics_exporter_host': 'http://localhost',
                'metrics_exporter_port': 4317,
                'tracing': True,
                'traces_exporter_host': 'http://localhost',
                'traces_exporter_port': 4317,
            }
        )
    return flow_dict


def get_flow_yaml(
    app: str,
    jcloud: bool = False,
    port: int = 8080,
    name: str = APP_NAME,
    is_websocket: bool = False,
    cors: bool = True,
    jcloud_config_path: str = None,
    env: str = None,
) -> str:
    return yaml.safe_dump(
        get_flow_dict(
            app=app,
            port=port,
            name=name,
            is_websocket=is_websocket,
            cors=cors,
            jcloud=jcloud,
            jcloud_config_path=jcloud_config_path,
            env=env,
        ),
        sort_keys=False,
    )


async def deploy_app_on_jcloud(
    flow_dict: Dict, app_id: str = None, verbose: bool = False
) -> Tuple[str, str]:
    os.environ['JCLOUD_LOGLEVEL'] = 'INFO' if verbose else 'ERROR'

    from jcloud.flow import CloudFlow

    with TemporaryDirectory() as tmpdir:
        flow_path = os.path.join(tmpdir, 'flow.yml')
        with open(flow_path, 'w') as f:
            yaml.safe_dump(flow_dict, f, sort_keys=False)

        deploy_envs = {'JCLOUD_HIDE_SUCCESS_MSG': 'true'} if not verbose else {}
        with EnvironmentVarCtxtManager(deploy_envs):
            if app_id is None:  # appid is None means we are deploying a new app
                jcloud_flow = await CloudFlow(path=flow_path).__aenter__()
                app_id = jcloud_flow.flow_id

            else:  # appid is not None means we are updating an existing app
                jcloud_flow = CloudFlow(path=flow_path, flow_id=app_id)
                await jcloud_flow.update()

        for k, v in jcloud_flow.endpoints.items():
            if k.lower() == 'gateway (http)' or k.lower() == 'gateway (websocket)':
                return app_id, v

    return None, None


async def patch_secret_on_jcloud(
    flow_dict: Dict, app_id: str, secret: str, verbose: bool = False
):
    os.environ['JCLOUD_LOGLEVEL'] = 'INFO' if verbose else 'ERROR'

    from jcloud.flow import CloudFlow

    with TemporaryDirectory() as tmpdir:
        flow_path = os.path.join(tmpdir, 'flow.yml')
        with open(flow_path, 'w') as f:
            yaml.safe_dump(flow_dict, f, sort_keys=False)

        deploy_envs = {'JCLOUD_HIDE_SUCCESS_MSG': 'true'} if not verbose else {}
        with EnvironmentVarCtxtManager(deploy_envs):
            jcloud_flow = CloudFlow(path=flow_path, flow_id=app_id)
            secrets_values = dict(dotenv_values(secret))
            await jcloud_flow.create_secret(
                secret_name=get_random_name(),
                env_secret_data=secrets_values,
                update=True,  # Important to update the Flow with the new secret
            )


async def get_app_status_on_jcloud(app_id: str):
    from jcloud.flow import CloudFlow
    from rich import box
    from rich.align import Align
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.table import Table

    _t = Table(
        'Attribute',
        'Value',
        show_header=False,
        box=box.ROUNDED,
        highlight=True,
        show_lines=True,
    )

    def _add_row(
        key,
        value,
        bold_key: bool = False,
        bold_value: bool = False,
        center_align: bool = True,
    ):
        return _t.add_row(
            Align(f'[bold]{key}' if bold_key else key, vertical='middle'),
            Align(f'[bold]{value}[/bold]' if bold_value else value, align='center')
            if center_align
            else value,
        )

    console = Console()
    with console.status(f'[bold]Getting app status for [green]{app_id}[/green]'):
        app_details = await CloudFlow(flow_id=app_id).status
        if app_details is None:
            return

        if 'status' not in app_details:
            return

        def _get_endpoint(app):
            endpoints = app.get('endpoints', {})
            return list(endpoints.values())[0] if endpoints else ''

        def _replace_wss_with_https(endpoint: str):
            return endpoint.replace('wss://', 'https://')

        status: Dict = app_details['status']
        total_cph = app_details.get('CPH', {}).get('total', 0)
        endpoint = _get_endpoint(status)

        _add_row('App ID', app_id, bold_key=True, bold_value=True)
        _add_row('Phase', status.get('phase', ''))
        _add_row('Endpoint', endpoint)
        _add_row(
            'App logs',
            Markdown(APP_LOGS_URL.format(app_id=app_id), justify='center'),
        )
        _add_row(
            'Base credits (per hour)',
            Markdown(PRICING_URL.format(cph=total_cph), justify='center'),
        )
        _add_row('Swagger UI', _replace_wss_with_https(f'{endpoint}/docs'))
        _add_row('OpenAPI JSON', _replace_wss_with_https(f'{endpoint}/openapi.json'))
        console.print(_t)


async def list_apps_on_jcloud(phase: str, name: str):
    from jcloud.flow import CloudFlow
    from jcloud.helper import cleanup_dt, get_phase_from_response
    from rich import box, print
    from rich.console import Console
    from rich.table import Table

    _t = Table(
        'AppID',
        'Phase',
        'Endpoint',
        'Created',
        box=box.ROUNDED,
        highlight=True,
    )

    console = Console()
    with console.status(f'[bold]Listing all apps'):
        all_apps = await CloudFlow().list_all(
            phase=phase, name=name, labels=f'app={DEFAULT_LABEL}'
        )
        if not all_apps:
            print('No apps found')
            return

        def _get_endpoint(app):
            endpoints = app.get('status', {}).get('endpoints', {})
            return list(endpoints.values())[0] if endpoints else ''

        for app in all_apps['flows']:
            _t.add_row(
                app['id'],
                get_phase_from_response(app),
                _get_endpoint(app),
                cleanup_dt(app['ctime']),
            )
        console.print(_t)


async def remove_app_on_jcloud(app_id: str) -> None:
    from jcloud.flow import CloudFlow
    from rich import print

    await CloudFlow(flow_id=app_id).__aexit__()
    print(f'App [bold][green]{app_id}[/green][/bold] removed successfully!')


async def serve_on_jcloud(
    app: str,
    app_dir: str = None,
    name: str = APP_NAME,
    uses: str = None,
    app_id: str = None,
    version: str = 'latest',
    timeout: int = DEFAULT_TIMEOUT,
    platform: str = None,
    config: str = None,
    cors: bool = True,
    env: str = None,
    secret: str = None,  # TODO: add support for secret
    verbose: bool = False,
    public: bool = False,
) -> str:
    from fastapi_serve.cloud.build import get_app_dir, push_app_to_hubble
    from fastapi_serve.cloud.config import resolve_jcloud_config
    from fastapi_serve.helper import get_random_tag

    app_dir, is_websocket = get_app_dir(app=app, app_dir=app_dir)
    config = resolve_jcloud_config(config=config, app_dir=app_dir)

    if uses is not None:
        # If `uses` is provided, use it as gateway id
        gateway_id = uses
    else:
        # If `uses` is not provided, push the app to hubble and get the gateway id
        gateway_id = push_app_to_hubble(
            app=app,
            app_dir=app_dir,
            tag=get_random_tag(),
            version=version,
            platform=platform,
            verbose=verbose,
            public=public,
        )

    # Get the flow dict
    flow_dict = get_flow_dict(
        app=app,
        jcloud=True,
        port=8080,
        name=name,
        timeout=timeout,
        app_id=app_id,
        gateway_id=gateway_id,
        is_websocket=is_websocket,
        jcloud_config_path=config,
        cors=cors,
        env=env,
    )

    # Deploy the app
    app_id, _ = await deploy_app_on_jcloud(
        flow_dict=flow_dict,
        app_id=app_id,
        verbose=verbose,
    )

    # If secret is not None, create a secret and update the app
    if secret is not None:
        await patch_secret_on_jcloud(
            flow_dict=flow_dict,
            app_id=app_id,
            secret=secret,
            verbose=verbose,
        )

    # Show the app status
    await get_app_status_on_jcloud(app_id=app_id)
    return app_id
