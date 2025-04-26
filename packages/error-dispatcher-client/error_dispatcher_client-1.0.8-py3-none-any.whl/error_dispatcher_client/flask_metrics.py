import uuid
import json
import time
import traceback

from flask import request, Flask
from .base_metrics import MetricsBase

class FlaskMetrics(MetricsBase):
    def init_app(self, app: Flask):
        """
        Middleware para capturar e enviar exceções e logs
        """
        @app.before_request
        def start_timer():
            """
            Armazena o tempo de início da requisição
            """
            request.start_time = time.time()

        @app.after_request
        def log_request(response):
            """
            Captura a requisição e registra informações de logs
            """
            try:
                duration = time.time() - getattr(request, "start_time", time.time())
                endpoint = request.endpoint
                method = request.method
                status_code = response.status_code

                self.logger.info(
                    f"Endpoint: {endpoint}, Method: {method}, Status: {status_code}, Duration: {duration:.4f}s"
                )
                return response
            except Exception as e:
                self.logger.error(f"Erro ao processar o log da requisição: {e}")
                return response

        @app.errorhandler(Exception)
        def handle_exception(e):
            """
            Captura exceções e registra informações detalhadas
            """
            try:
                app_name = self.app_name if self.app_name else request.base_url
                duration = time.time() - getattr(request, "start_time", time.time())

                try:
                    body = request.get_data(as_text=True)
                    decoded_body = json.loads(body) if request.content_type == "application/json" else body
                except Exception:
                    decoded_body = "Unable to parse body"

                error_data = {
                    "app_name": app_name,
                    "endpoint": request.endpoint,
                    "full_url": request.url,
                    "method": request.method,
                    "status_code": 500,
                    "duration": duration,
                    "headers": dict(request.headers),
                    "query_params": request.args.to_dict(),
                    "request_body": decoded_body,
                    "client_ip": request.remote_addr,
                    "user_agent": request.headers.get("User-Agent", "N/A"),
                    "error_details": str(e),
                    "error_type": type(e).__name__,
                    "traceback": traceback.format_exc(),
                    "timestamp": time.time_ns() // 1_000_000,
                    "guid_error": str(uuid.uuid4())
                }

                self.logger.error(error_data)
                self.send_to_providers(error_data)

            except Exception as logging_error:
                self.logger.error(f"Erro ao registrar exceção: {logging_error}")

            return {"error": "Internal Server Error"}, 500
