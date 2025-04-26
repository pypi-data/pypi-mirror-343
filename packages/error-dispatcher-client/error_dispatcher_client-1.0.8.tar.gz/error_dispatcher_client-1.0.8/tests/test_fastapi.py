import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from error_dispatcher_client import FastAPIMetrics
from error_dispatcher_client.providers import KafkaProvider

def test_fastapi_metrics():
    app = FastAPI()
    kafka_provider = KafkaProvider(bootstrap_servers="localhost:9092", topic="errors")
    metrics = FastAPIMetrics(providers=[kafka_provider])
    metrics.init_app(app)

    @app.get("/")
    async def index():
        raise ValueError("Teste de erro")

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 500
