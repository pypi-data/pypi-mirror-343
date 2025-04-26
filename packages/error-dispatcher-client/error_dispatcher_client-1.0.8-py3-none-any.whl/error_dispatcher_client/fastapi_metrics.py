import uuid
import json
import time
import traceback

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .base_metrics import MetricsBase

class FastAPIMetrics(MetricsBase):
    def init_app(self, app: FastAPI):
        """
        Configura o middleware e o manipulador global de exceções.
        """
        @app.middleware("http")
        async def log_requests(request: Request, call_next):
            """
            Middleware para capturar requests e erros.
            """
            start_time = time.time()
            uuid_log = uuid.uuid4().__str__()
            setattr(request, "uuid", uuid_log)
            try:
                response = await call_next(request)
                self.log_request_data(request, response, start_time, None)
                return response
            except Exception as e:
                return await self.handle_exception(request, e, start_time)

        @app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            """
            Manipulador global para HTTPException.
            """
            start_time = time.time()
            return await self.handle_exception(request, exc, start_time)

    async def handle_exception(self, request: Request, exception: Exception, start_time: float):
        """
        Lida com exceções, registra os detalhes e envia para os provedores.
        """
        duration = time.time() - start_time
        app_name = self.app_name if self.app_name else request.base_url

        try:
            body = await request.body()
            decoded_body = body.decode('utf-8', errors='ignore')
        except Exception:
            decoded_body = "Unable to parse body"

        error_data = {
            "app_name": app_name,
            "uuid": getattr(request, 'uuid', None),
            "endpoint": request.url.path,
            "full_url": str(request.url),
            "method": request.method,
            "status_code": getattr(exception, 'status_code', 500),
            "duration": duration,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
            "request_body": str(json.loads(await request.body())) if request.headers.get("Content-Type")
                                == "application/json" else decoded_body,
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent", "N/A"),
            "error_details": getattr(exception, 'detail', str(exception)),
            "error_type": type(exception).__name__,
            "traceback": traceback.format_exc(),
            "timestamp": time.time_ns() // 1_000_000,
            "guid_error": str(uuid.uuid4())
        }

        self.log_request_data(request, None, start_time, exception)
        self.send_to_providers(error_data)

        return JSONResponse(content=getattr(exception, 'detail', "Internal Server Error")
                            ,status_code=getattr(exception, 'status_code', 500))

    def log_request_data(self, request: Request, response, start_time: float, exception: Exception):
        """
        Registra os detalhes da request e da response.
        """

        duration = time.time() - start_time
        endpoint = request.url.path
        method = request.method
        status_code = response.status_code if response else 500
        uuid_log = getattr(request, 'uuid', None)

        log_message = {
            "endpoint": endpoint,
            "method": method,
            "status": status_code,
            "duration": f"{duration:.4f}s",
            "uuid": uuid_log
        }

        if exception:
            log_message.update({
                "error_details": getattr(exception, 'detail', str(exception)),
                "error_type": type(exception).__name__,
            })
            self.logger.error(log_message)
        elif status_code < 400:
            self.logger.info(log_message)
