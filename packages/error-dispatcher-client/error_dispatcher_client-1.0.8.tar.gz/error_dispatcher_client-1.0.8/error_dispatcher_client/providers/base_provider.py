import logging
from error_dispatcher_client.templates import TemplateBase

class ErrorProvider:
    """
    Classe base Provider
    """
    def __init__(self, message_template: TemplateBase, logging_custom : logging.Logger = None):
        if logging_custom is None:
            self.logger = logging.getLogger("MetricsBase")
            logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t  %(asctime)s - %(message)s")
        elif isinstance(logging_custom, logging.Logger):
            self.logger = logging_custom
        else:
            raise TypeError(
                f"logging_custom deve ser um objeto 'logging.Logger',"
                f"mas recebeu {type(logging_custom).__name__}")

        self.message_template = message_template if message_template else TemplateBase()


    def send(self, error_data: dict):
        """
        Metodo que deve ser implementado por cada provedor.
        """
        raise NotImplementedError("O metodo `send` deve ser implementado.")
