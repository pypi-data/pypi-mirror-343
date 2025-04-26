import pytest
from flask import Flask
from error_dispatcher_client import FlaskMetrics, KafkaProvider

def test_flask_metrics():
    app = Flask(__name__)
    kafka_provider = KafkaProvider(bootstrap_servers="localhost:9092", topic="errors")
    metrics = FlaskMetrics(providers=[kafka_provider])
    metrics.init_app(app)

    @app.route("/")
    def index():
        raise ValueError("Teste de erro")

    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 500
