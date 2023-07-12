import asyncio
import importlib
import os
import time
import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

if TYPE_CHECKING:
    from jina.logging.logger import JinaLogger
    from opentelemetry.sdk.metrics import Counter
    from starlette.types import ASGIApp, Receive, Scope, Send


APPDIR = "/appdir"


class ImportFromStringError(Exception):
    pass


def import_from_string(import_str: Any) -> Tuple[Any, Any]:
    if not isinstance(import_str, str):
        return import_str

    module_str, _, attrs_str = import_str.partition(":")
    if not module_str or not attrs_str:
        message = (
            'Import string "{import_str}" must be in format "<module>:<attribute>".'
        )
        raise ImportFromStringError(message.format(import_str=import_str))

    try:
        module = importlib.import_module(module_str)
    except ImportError as exc:
        if exc.name != module_str:
            raise exc from None
        message = 'Could not import module "{module_str}".'
        raise ImportFromStringError(message.format(module_str=module_str))

    app = module
    try:
        for attr_str in attrs_str.split("."):
            app = getattr(app, attr_str)
    except AttributeError:
        message = 'Attribute "{attrs_str}" not found in module "{module_str}".'
        raise ImportFromStringError(
            message.format(attrs_str=attrs_str, module_str=module_str)
        )

    return app, module


class Timer:
    class SharedData:
        def __init__(self, last_reported_time):
            self.last_reported_time = last_reported_time

    def __init__(self, interval: int):
        self.interval = interval

    async def send_duration_periodically(
        self,
        shared_data: SharedData,
        route: str,
        protocol: str,
        counter: Optional["Counter"] = None,
    ):
        while True:
            await asyncio.sleep(self.interval)
            current_time = time.perf_counter()
            if counter:
                counter.add(
                    current_time - shared_data.last_reported_time,
                    {"route": route, "protocol": protocol},
                )

            shared_data.last_reported_time = current_time


class MetricsMiddleware:
    def __init__(
        self,
        app: "ASGIApp",
        duration_counter: Optional["Counter"] = None,
        request_counter: Optional["Counter"] = None,
    ):
        self.app = app
        self.duration_counter = duration_counter
        self.request_counter = request_counter
        # TODO: figure out solution for static assets
        self.skip_routes = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/healthz",
            "/dry_run",
            "/metrics",
            "/favicon.ico",
        ]

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        # Not all Scope objs have path key, e.g., lifespan type of scope
        path = scope.get("path")
        if path and path not in self.skip_routes:
            timer = Timer(5)
            shared_data = timer.SharedData(last_reported_time=time.perf_counter())
            send_duration_task = asyncio.create_task(
                timer.send_duration_periodically(
                    shared_data, path, scope["type"], self.duration_counter
                )
            )
            try:
                await self.app(scope, receive, send)
            finally:
                send_duration_task.cancel()
                if self.duration_counter:
                    self.duration_counter.add(
                        time.perf_counter() - shared_data.last_reported_time,
                        {"route": path, "protocol": scope["type"]},
                    )
                if self.request_counter:
                    self.request_counter.add(
                        1, {"route": path, "protocol": scope["type"]}
                    )
        else:
            await self.app(scope, receive, send)


class LoggingMiddleware:
    def __init__(self, app: "ASGIApp", logger: "JinaLogger"):
        self.app = app
        self.logger = logger
        self.skip_routes = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/healthz",
            "/dry_run",
            "/metrics",
            "/favicon.ico",
        ]

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        # Not all Scope objs have path key, e.g., lifespan type of scope
        path = scope.get("path")
        if path and path not in self.skip_routes:
            # Get IP address, use X-Forwarded-For if set else use scope['client'][0]
            ip_address = scope.get("client")[0] if scope.get("client") else None
            if scope.get("headers"):
                for header in scope["headers"]:
                    if header[0].decode("latin-1") == "x-forwarded-for":
                        ip_address = header[1].decode("latin-1").split(",")[0].strip()
                        break

            # Init the request/connection ID
            request_id = str(uuid.uuid4()) if scope["type"] == "http" else None
            connection_id = str(uuid.uuid4()) if scope["type"] == "websocket" else None

            status_code = None
            start_time = time.perf_counter()

            async def custom_send(message: dict) -> None:
                nonlocal status_code

                # TODO: figure out a way to do the same for ws
                if request_id and message.get("type") == "http.response.start":
                    message.setdefault("headers", []).append(
                        (b"X-API-Request-ID", str(request_id).encode())
                    )
                    status_code = message.get("status")

                await send(message)

            await self.app(scope, receive, custom_send)

            end_time = time.perf_counter()
            duration = round(end_time - start_time, 3)

            if scope["type"] == "http":
                self.logger.info(
                    f"HTTP request: {request_id} - Path: {path} - Client IP: {ip_address} - Status code: {status_code} - Duration: {duration} s"
                )
            elif scope["type"] == "websocket":
                self.logger.info(
                    f"WebSocket connection: {connection_id} - Path: {path} - Client IP: {ip_address} - Duration: {duration} s"
                )

        else:
            await self.app(scope, receive, send)
