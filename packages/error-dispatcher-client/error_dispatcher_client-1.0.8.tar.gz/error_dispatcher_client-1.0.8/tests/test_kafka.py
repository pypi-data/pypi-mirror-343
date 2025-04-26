from error_dispatcher_client.providers import KafkaProvider

def test_kafka_provider(mocker):
    mock_producer = mocker.patch("kafka.KafkaProducer")
    provider = KafkaProvider(bootstrap_servers="localhost:9092", topic="errors")
    provider.send({"error": "Teste"})
    mock_producer().send.assert_called_once()
