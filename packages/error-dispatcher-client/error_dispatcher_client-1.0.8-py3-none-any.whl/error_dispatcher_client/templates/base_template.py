from dataclasses import dataclass

@dataclass
class TemplateBase:
    def __init__(self):
        """
        Template base para mensagem de error
        """
        self.app_name = None,
        self.uuid = None
        self.endpoint = None,
        self.full_url = None,
        self.method = None,
        self.status_code = None,
        self.duration = None,
        self.headers = None,
        self.query_params = None,
        self.request_body = None,
        self.client_ip = None,
        self.user_agent = None,
        self.error_details = None,
        self.error_type = None,
        self.traceback = None
        self.timestamp = None
        self.guid_error = None

    def update(self, data: dict):
        """
        Atualiza os atributos da classe com os dados fornecidos.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def as_dict(self):
        """
        retorna a o template como dicionario
        """
        return {key: value for key, value in vars(self).items()}


class CustomTemplate(TemplateBase):
    def __init__(self, attributes_to_keep : dict):
        super().__init__()

        for attr in list(vars(self).keys()):
            if attr not in attributes_to_keep:
                delattr(self, attr)

        for attr, value in attributes_to_keep.items():
            if not hasattr(self, attr):
                setattr(self, attr, value)