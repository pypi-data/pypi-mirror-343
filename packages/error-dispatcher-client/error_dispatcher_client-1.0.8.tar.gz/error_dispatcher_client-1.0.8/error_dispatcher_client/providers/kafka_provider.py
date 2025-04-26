import json
from confluent_kafka import Producer
from .base_provider import ErrorProvider
from error_dispatcher_client.templates import TemplateBase

class KafkaProvider(ErrorProvider):
    def __init__(self, bootstrap_servers, topic, message_template: TemplateBase = None):
        """
        Inicializa o producer Kafka
        """
        super().__init__(message_template=message_template)
        self.producer = Producer(
            {
                "bootstrap.servers": bootstrap_servers,
                'message.send.max.retries': 1,
                'retry.backoff.ms': 1000,
                'socket.max.fails': 1,
                'reconnect.backoff.max.ms': 2000,
                'log.connection.close': False,
            }
        )
        self.topic = topic

    def send(self, error_data: dict):
        try:
            self.message_template.update(error_data)
            error_data = self.message_template.as_dict()
            json_data = json.dumps(error_data).encode("utf-8")
            self.producer.produce(self.topic, value=json_data)
            self.producer.flush()
        except Exception as e:
            self.logger.error(f"Erro ao enviar mensagem para o Kafka: {e}")