import asyncio
import os
import uuid
from functools import wraps
from typing import Dict

import nest_asyncio

try:
    nest_asyncio.apply()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        nest_asyncio.apply()
    except RuntimeError:
        pass


def syncify(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def get_random_name():
    return 'f-' + uuid.uuid4().hex[:6]


def get_random_tag():
    return 't-' + uuid.uuid4().hex[:5]


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def asyncio_run(func, *args, **kwargs):
    return get_or_create_eventloop().run_until_complete(func(*args, **kwargs))


def asyncio_run_property(func):
    task = asyncio.ensure_future(func)
    get_or_create_eventloop().run_until_complete(task)
    return task.result()


class EnvironmentVarCtxtManager:
    """a class to wrap env vars"""

    def __init__(self, envs: Dict):
        """
        :param envs: a dictionary of environment variables
        """
        self._env_keys_added: Dict = envs
        self._env_keys_old: Dict = {}

    def __enter__(self):
        for key, val in self._env_keys_added.items():
            # Store the old value, if it exists
            if key in os.environ:
                self._env_keys_old[key] = os.environ[key]
            # Update the environment variable with the new value
            os.environ[key] = str(val)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the old values of updated environment variables
        for key, val in self._env_keys_old.items():
            os.environ[key] = str(val)
        # Remove any newly added environment variables
        for key in self._env_keys_added.keys():
            os.unsetenv(key)
