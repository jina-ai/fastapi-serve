import os
from functools import lru_cache

import requests
from hubble import Auth

HubbleAPI = "https://api.hubble.jina.ai/v2/rpc/"
HubbleGetUserAPI = HubbleAPI + "user.session.getUser"
FlowUserEnvVar = "JINA_FLOW_USER_ID"


@lru_cache
def get_jina_userid(token: str = None) -> str:
    """Get the Jina user id from the Hubble API."""
    if token is None:
        token = Auth().get_auth_token()

    response = requests.post(
        HubbleGetUserAPI,
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get user id from Hubble: {response.text}")

    _json = response.json()
    return _json.get("data", {}).get("_id", '<unknown>')


def get_userid_from_env():
    return os.environ.get(FlowUserEnvVar, None)


def authorize(token: str) -> bool:
    """Authorize the user with the Hubble API."""
    try:
        return get_jina_userid(token) == get_userid_from_env()
    except Exception as e:
        print(e)
        return False
