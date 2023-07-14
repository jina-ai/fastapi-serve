from typing import Callable, List, Optional

from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from fastapi_serve.utils.helper import authorize


class JinaAuthBase:
    SKIPPED_PATHS = ['/', '/docs', '/openapi.json']

    def __init__(
        self,
        app: Optional[ASGIApp] = None,
        exclude_paths: Optional[List[str]] = None,
    ):
        self.exclude_paths = set(exclude_paths or []) | set(self.SKIPPED_PATHS)

    async def validate_request(self, request: Request):
        if request.url.path not in self.exclude_paths:
            header = request.headers.get('Authorization')
            if not header:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Missing authorization header',
                )

            try:
                scheme, token = header.split()
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid authorization header format',
                )
            if scheme.lower() != 'bearer':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid scheme',
                )

            if not authorize(token):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid token',
                )
        return request


class JinaAuthDependency(JinaAuthBase):
    async def __call__(self, request: Request):
        return await self.validate_request(request)


class JinaAuthMiddleware(JinaAuthBase, BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, exclude_paths: Optional[List[str]] = None):
        JinaAuthBase.__init__(self, app=app, exclude_paths=exclude_paths)
        BaseHTTPMiddleware.__init__(self, app)

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            await self.validate_request(request)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'detail': e.detail})
        response = await call_next(request)
        return response


JinaAPIKeyHeader = APIKeyHeader(name="Authorization", auto_error=False)

__all__ = ['JinaAuthDependency', 'JinaAuthMiddleware', 'JinaAPIKeyHeader']
