import os
import secrets
import sys
from http import HTTPStatus
from shutil import copyfile, copytree
from tempfile import mkdtemp
from typing import Optional, Tuple

import requests
import yaml

from fastapi_serve.cloud.helper import (
    any_websocket_route_in_app,
    get_parent_dir,
    load_fastapi_app,
)
from fastapi_serve.helper import get_random_name


def hubble_exists(name: str, secret: Optional[str] = None) -> bool:
    return (
        requests.get(
            url='https://api.hubble.jina.ai/v2/executor/getMeta',
            params={'id': name, 'secret': secret},
        ).status_code
        == HTTPStatus.OK
    )


def get_jinaai_uri(id: str, tag: str):
    import requests
    from hubble import Auth

    r = requests.get(
        f"https://apihubble.jina.ai/v2/executor/getMeta?id={id}&tag={tag}",
        headers={"Authorization": f"token {Auth.get_auth_token()}"},
    )
    _json = r.json()
    if _json is None:
        print(f'Could not find image with id {id} and tag {tag}')
        return
    _image_name = _json['data']['name']
    _user_name = _json['meta']['owner']['name']
    return f'jinaai+docker://{_user_name}/{_image_name}:{tag}'


def get_app_dir(app: str, app_dir: str = None) -> Tuple[str, bool]:
    sys.path.insert(0, os.getcwd())

    _fastapi_app, _module = load_fastapi_app(app)
    _is_websocket = any_websocket_route_in_app(_fastapi_app)

    # if app_dir is not None, return it
    if app_dir is not None:
        return app_dir, _is_websocket
    else:
        return get_parent_dir(modname=app, filename=_module.__file__), _is_websocket


def _remove_fastapi_serve(tmpdir: str) -> None:
    _requirements_txt = 'requirements.txt'
    _pyproject_toml = 'pyproject.toml'

    # Remove fastapi-serve itself from the requirements list as a fixed version might break things
    if os.path.exists(os.path.join(tmpdir, _requirements_txt)):
        with open(os.path.join(tmpdir, _requirements_txt), 'r') as f:
            reqs = f.read().splitlines()

        reqs = [r for r in reqs if not r.startswith("fastapi-serve")]
        with open(os.path.join(tmpdir, _requirements_txt), 'w') as f:
            f.write('\n'.join(reqs))

    if os.path.exists(os.path.join(tmpdir, _pyproject_toml)):
        import toml

        with open(os.path.join(tmpdir, _pyproject_toml), 'r') as f:
            pyproject = toml.load(f)

        if 'tool' in pyproject and 'poetry' in pyproject['tool']:
            poetry = pyproject['tool']['poetry']
            if 'dependencies' in poetry:
                poetry['dependencies'] = {
                    k: v
                    for k, v in poetry['dependencies'].items()
                    if k != 'fastapi-serve'
                }

            if 'dev-dependencies' in poetry:
                poetry['dev-dependencies'] = {
                    k: v
                    for k, v in poetry['dev-dependencies'].items()
                    if k != 'fastapi-serve'
                }

        with open(os.path.join(tmpdir, _pyproject_toml), 'w') as f:
            toml.dump(pyproject, f)


def _handle_dependencies(reqs: Tuple[str], tmpdir: str):
    # Create the requirements.txt if requirements are given
    _requirements_txt = 'requirements.txt'
    _pyproject_toml = 'pyproject.toml'

    _existing_requirements = []
    # Get existing requirements and add the new ones
    if os.path.exists(os.path.join(tmpdir, _requirements_txt)):
        with open(os.path.join(tmpdir, _requirements_txt), 'r') as f:
            _existing_requirements = tuple(f.read().splitlines())

    _new_requirements = []
    if reqs is not None:
        for _req in reqs:
            if os.path.isdir(_req):
                if os.path.exists(os.path.join(_req, _requirements_txt)):
                    with open(os.path.join(_req, _requirements_txt), 'r') as f:
                        _new_requirements = f.read().splitlines()

                elif os.path.exists(os.path.join(_req, _pyproject_toml)):
                    # copy pyproject.toml to tmpdir
                    copyfile(
                        os.path.join(_req, _pyproject_toml),
                        os.path.join(tmpdir, _pyproject_toml),
                    )
            elif os.path.isfile(_req):
                # if it's a file and name is requirements.txt, read it
                if os.path.basename(_req) == _requirements_txt:
                    with open(_req, 'r') as f:
                        _new_requirements = f.read().splitlines()
                elif os.path.basename(_req) == _pyproject_toml:
                    # copy pyproject.toml to tmpdir
                    copyfile(_req, os.path.join(tmpdir, _pyproject_toml))
            else:
                _new_requirements.append(_req)

        _final_requirements = set(_existing_requirements).union(set(_new_requirements))
        with open(os.path.join(tmpdir, _requirements_txt), 'w') as f:
            f.write('\n'.join(_final_requirements))

    _remove_fastapi_serve(tmpdir)


def _handle_dockerfile(tmpdir: str, version: str):
    # if file `fastapi-serve.Dockefile` exists, use it
    _fastapi_serve_dockerfile = 'fastapi-serve.Dockerfile'
    if os.path.exists(os.path.join(tmpdir, _fastapi_serve_dockerfile)):
        copyfile(
            os.path.join(tmpdir, _fastapi_serve_dockerfile),
            os.path.join(tmpdir, 'Dockerfile'),
        )

        # read the Dockerfile and replace the version
        with open(os.path.join(tmpdir, 'Dockerfile'), 'r') as f:
            dockerfile = f.read()

        dockerfile = dockerfile.replace(
            'jinawolf/fastapi-serve:${version}',
            f'jinawolf/fastapi-serve:{version}',
        )

        if 'ENTRYPOINT' not in dockerfile:
            dockerfile = (
                dockerfile
                + '\nENTRYPOINT [ "jina", "gateway", "--uses", "config.yml" ]'
            )

        with open(os.path.join(tmpdir, 'Dockerfile'), 'w') as f:
            f.write(dockerfile)

    else:
        # Create the Dockerfile
        with open(os.path.join(tmpdir, 'Dockerfile'), 'w') as f:
            dockerfile = [
                f'FROM jinawolf/fastapi-serve:{version}',
                'COPY . /appdir/',
                'RUN if [ -e /appdir/requirements.txt ]; then pip install -r /appdir/requirements.txt; fi',
                'ENTRYPOINT [ "jina", "gateway", "--uses", "config.yml" ]',
            ]
            f.write('\n\n'.join(dockerfile))


def _handle_config_yaml(tmpdir: str, name: str):
    # Create the config.yml
    with open(os.path.join(tmpdir, 'config.yml'), 'w') as f:
        config_dict = {
            'jtype': 'FastAPIServeGateway',
            'py_modules': ['fastapi_serve/gateway/__init__.py'],
            'metas': {
                'name': name,
            },
        }
        f.write(yaml.safe_dump(config_dict, sort_keys=False))


def _push_to_hubble(
    tmpdir: str, name: str, tag: str, platform: str, verbose: bool, public: bool
) -> str:
    from hubble.executor.hubio import HubIO
    from hubble.executor.parsers import set_hub_push_parser

    from fastapi_serve.helper import EnvironmentVarCtxtManager

    secret = secrets.token_hex(8)
    args_list = [
        tmpdir,
        '--tag',
        tag,
        '--no-usage',
        '--no-cache',
    ]
    if verbose:
        args_list.remove('--no-usage')
        args_list.append('--verbose')
    if not public:
        args_list.append('--secret')
        args_list.append(secret)
        args_list.append('--private')

    args = set_hub_push_parser().parse_args(args_list)

    if platform:
        args.platform = platform

    if hubble_exists(name, secret):
        args.force_update = name

    push_envs = (
        {'JINA_HUBBLE_HIDE_EXECUTOR_PUSH_SUCCESS_MSG': 'true'} if not verbose else {}
    )
    with EnvironmentVarCtxtManager(push_envs):
        gateway_id = HubIO(args).push().get('id')
        return gateway_id + ':' + tag


def push_app_to_hubble(
    app: str,
    app_dir: str = None,
    image_name: str = None,
    tag: str = 'latest',
    version: str = 'latest',
    platform: str = None,
    verbose: Optional[bool] = False,
    public: Optional[bool] = False,
) -> str:
    tmpdir = mkdtemp()
    app_dir, _ = get_app_dir(app=app, app_dir=app_dir)

    # Copy appdir to tmpdir
    copytree(app_dir, tmpdir, dirs_exist_ok=True)
    # Copy fastapi_serve to tmpdir
    copytree(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        os.path.join(tmpdir, 'fastapi_serve'),
        dirs_exist_ok=True,
    )

    if image_name is None:
        image_name = get_random_name()
    _remove_fastapi_serve(tmpdir)
    _handle_dockerfile(tmpdir, version)
    _handle_config_yaml(tmpdir, image_name)
    return _push_to_hubble(tmpdir, image_name, tag, platform, verbose, public)
