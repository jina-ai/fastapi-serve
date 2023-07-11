import asyncio
import sys
import uuid
from functools import wraps
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from types import ModuleType

    from fastapi import FastAPI


def syncify(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def get_random_name():
    return 'f-' + uuid.uuid4().hex[:6]


def load_fastapi_app(app_str: str) -> Tuple['FastAPI', 'ModuleType']:
    from fastapi_serve.gateway.helper import ImportFromStringError, import_from_string

    try:
        app, module = import_from_string(app_str)
    except ImportFromStringError as e:
        print(f'Could not import app from {app_str}: {e}')
        sys.exit(1)

    return app, module


def any_websocket_route_in_app(app: 'FastAPI') -> bool:
    from fastapi.routing import APIWebSocketRoute

    return any(isinstance(r, APIWebSocketRoute) for r in app.routes)


def get_parent_dir(modname: str, filename: str) -> str:
    parts = modname.split('.')
    parent_dir = os.path.dirname(filename)
    for _ in range(len(parts) - 1):
        parent_dir = os.path.dirname(parent_dir)
    return parent_dir
