import os
import sys
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING

from jina.serve.runtimes.gateway.http.fastapi import FastAPIBaseGateway

from fastapi_serve.gateway.helper import (
    APPDIR,
    LoggingMiddleware,
    MetricsMiddleware,
    import_from_string,
)
from fastapi_serve.helper import EnvironmentVarCtxtManager

if TYPE_CHECKING:
    from fastapi import FastAPI


class FastAPIServeGateway(FastAPIBaseGateway):
    def __init__(self, app: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app_str = app
        self._app: "FastAPI" = None
        self._fix_sys_path()
        self._init_fastapi_app()
        self._configure_cors()
        self._register_healthz()
        self._setup_metrics()
        self._setup_logging()

    @property
    def app(self) -> "FastAPI":
        return self._app

    @cached_property
    def workspace(self) -> str:
        import tempfile

        _temp_dir = tempfile.mkdtemp()
        if "FLOW_ID" not in os.environ:
            self.logger.debug(f"Using temporary workspace directory: {_temp_dir}")
            return _temp_dir

        try:
            flow_id = os.environ["FLOW_ID"]
            namespace = flow_id.split("-")[-1]
            return os.path.join("/data", f"jnamespace-{namespace}")
        except Exception as e:
            self.logger.warning(f"Failed to get workspace directory: {e}")
            return _temp_dir

    def _init_fastapi_app(self):
        with EnvironmentVarCtxtManager({'JCLOUD_WORKSPACE': self.workspace}):
            self.logger.info(f"Loading app from {self._app_str}")
            self._app, _ = import_from_string(self._app_str)

    def _configure_cors(self):
        if self.cors:
            if any(
                [
                    isinstance(middleware, CORSMiddleware)
                    for middleware in self._app.user_middleware
                ]
            ):
                self.logger.warning("CORS is already enabled")
                return

            else:
                self.logger.info("Enabling CORS")
                from fastapi.middleware.cors import CORSMiddleware

                self._app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )

    def _fix_sys_path(self):
        if os.getcwd() not in sys.path:
            sys.path.append(os.getcwd())

        if Path(APPDIR).exists() and APPDIR not in sys.path:
            # This is where the app code is mounted in the container
            sys.path.append(APPDIR)

    def _setup_metrics(self):
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        if not self.meter_provider:
            self.http_duration_counter = None
            self.ws_duration_counter = None
            return

        FastAPIInstrumentor.instrument_app(
            self._app,
            meter_provider=self.meter_provider,
            tracer_provider=self.tracer_provider,
        )

        self.duration_counter = self.meter.create_counter(
            name="fastapi_serve_request_duration_seconds",
            description="FastAPI-serve Request duration in seconds",
            unit="s",
        )

        self.request_counter = self.meter.create_counter(
            name="fastapi_serve_request_count",
            description="FastAPI-serve Request count",
        )

        self.app.add_middleware(
            MetricsMiddleware,
            duration_counter=self.duration_counter,
            request_counter=self.request_counter,
        )

    def _setup_logging(self):
        self.app.add_middleware(LoggingMiddleware, logger=self.logger)

    def _register_healthz(self):
        @self.app.get("/healthz")
        async def __healthz():
            return {"status": "ok"}

        @self.app.get("/dry_run")
        async def __dry_run():
            return {"status": "ok"}

    def _update_dry_run_with_ws(self):
        """Update the dry_run endpoint to a websocket endpoint"""
        from fastapi import WebSocket
        from fastapi.routing import APIRoute

        for route in self.app.routes:
            if route.path == "/dry_run" and isinstance(route, APIRoute):
                self.app.routes.remove(route)
                break

        @self.app.websocket("/dry_run")
        async def __dry_run(websocket: WebSocket):
            await websocket.accept()
            await websocket.send_json({"status": "ok"})
            await websocket.close()
