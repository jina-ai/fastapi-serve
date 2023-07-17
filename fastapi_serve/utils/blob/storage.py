from io import BytesIO
from typing import Dict, Union

from fastapi import UploadFile as FastAPIUploadFile
from hubble import Client
from starlette.datastructures import UploadFile as StarletteUploadFile

JINAAI_PREFIX = 'jinaai://'


class InvalidURI(Exception):
    pass


class JinaBlobStorage:
    # TODO: add support for real-async for hubble client
    @staticmethod
    async def upload(
        file: Union[str, BytesIO, FastAPIUploadFile, StarletteUploadFile],
        name: str,
        metadata: Dict = {},
        public: bool = False,
    ):
        if isinstance(file, (FastAPIUploadFile, StarletteUploadFile)):
            file = BytesIO(await file.read())

        # if name has suffix, remove it to adhere to regexp: ^[a-zA-Z][-a-zA-Z0-9_]{3,255}$..
        if '.' in name:
            name = name[: name.rfind('.')]

        r = Client().upload_artifact(
            f=file,
            name=name,
            metadata=metadata,
            is_public=public,
        )
        r.raise_for_status()
        _id = r.json().get('data', {}).get('_id')
        if not _id:
            raise Exception('Failed to upload artifact')

        return JINAAI_PREFIX + _id

    @staticmethod
    async def download(uri: str, file: Union[str, BytesIO]) -> None:
        if not uri.startswith(JINAAI_PREFIX):
            raise InvalidURI(f'Invalid uri: {uri}')

        _id = uri.replace(JINAAI_PREFIX, '')
        Client().download_artifact(id=_id, f=file)
        print(f'Downloaded artifact to {file}')

    @staticmethod
    async def get_info(uri: str) -> Dict:
        if not uri.startswith(JINAAI_PREFIX):
            raise InvalidURI(f'Invalid uri: {uri}')

        _id = uri.replace(JINAAI_PREFIX, '')

        r = Client().get_artifact_info(id=_id)
        r.raise_for_status()
        return r.json().get('data', {})

    @staticmethod
    async def list() -> Dict:
        # TODO: add filters
        r = Client().list_artifacts()
        r.raise_for_status()
        return r.json().get('data', {})

    @staticmethod
    async def delete(uri: str) -> None:
        if not uri.startswith(JINAAI_PREFIX):
            raise InvalidURI(f'Invalid uri: {uri}')

        _id = uri.replace(JINAAI_PREFIX, '')
        r = Client().delete_artifact(id=_id)
        r.raise_for_status()
        print(f'Deleted artifact with id {_id}')
