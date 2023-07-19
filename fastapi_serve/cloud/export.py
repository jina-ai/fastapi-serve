import os
from enum import Enum
from pathlib import Path


class ExportKind(str, Enum):
    KUBERNETES = 'kubernetes'
    DOCKER_COMPOSE = 'docker-compose'


async def export_app(
    app: str,
    kind: ExportKind,
    path: str,
    app_dir: str = None,
    uses: str = None,
    version: str = 'latest',
    platform: str = None,
    cors: bool = True,
    env: str = None,
    verbose: bool = False,
    public: bool = True,
) -> str:
    from jina import Flow

    from fastapi_serve.cloud.build import get_app_dir, push_app_to_hubble
    from fastapi_serve.cloud.deploy import get_flow_dict
    from fastapi_serve.helper import get_random_tag

    app_dir, is_websocket = get_app_dir(app=app, app_dir=app_dir)

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
            public=True,  # TODO: add support for private images during export
        )

    # Get the flow dict
    flow_dict = get_flow_dict(
        app=app,
        jcloud=True,
        port=8080,
        app_id=None,
        gateway_id=gateway_id,
        is_websocket=is_websocket,
        jcloud_config_path=None,
        cors=cors,
        env=env,
    )

    # Load the Flow & export it
    f: Flow = Flow.load_config(flow_dict)

    if kind == ExportKind.KUBERNETES:
        f.to_kubernetes_yaml(path)
    elif kind == ExportKind.DOCKER_COMPOSE:
        _path = Path(path)
        if _path.is_file() and _path.suffix in ['.yml', '.yaml']:
            f.to_docker_compose_yaml(path)
        elif _path.is_dir():
            f.to_docker_compose_yaml(os.path.join(path, 'docker-compose.yml'))
        else:
            raise ValueError('path must be a file or a directory')
