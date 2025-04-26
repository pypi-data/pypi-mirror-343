
---

# 🔥 error_dispatcher_client

**`error_dispatcher_client`** é um pacote Python poderoso para rastreamento e tratamento de erros em aplicações web. Ele captura exceções ocorridas em APIs desenvolvidas com **Flask** ou **FastAPI** e permite enviar relatórios de erros para diversos provedores, como **Kafka**, **Discord** e **E-mail**. Com suporte a múltiplos provedores simultâneos, é fácil adaptar o pacote às suas necessidades específicas.

---

## ✨ Principais Funcionalidades

- **Captura automática de exceções** em endpoints de **Flask** e **FastAPI**.
- **Suporte a múltiplos provedores** para notificação:
  - **Kafka**: Envia mensagens de erro para um tópico Kafka.
  - **Discord**: Envia mensagens de erro via webhook
  - **E-mail**: Envia relatórios detalhados via SMTP.
  - **Fácil extensão** para novos provedores personalizados.
- Configuração simples e integração prática.

---

## 🛠️ Instalação

```bash
pip install error_dispather_client
```

---

## 🚀 Como Usar

### Com Flask

```python
from flask import Flask
from error_dispatcher_client import FlaskMetrics
from error_dispatcher_client.providers import KafkaProvider, EmailProvider

app = Flask(__name__)

kafka_provider = KafkaProvider(bootstrap_servers="localhost:9092", topic="errors")
email_provider = EmailProvider(
  smtp_server="smtp.gmail.com",
  smtp_port=587,
  username="seuemail@gmail.com",
  password="suasenha"
)

metrics = FlaskMetrics(providers=[kafka_provider, email_provider])
metrics.init_app(app)


@app.route("/")
def index():
  raise ValueError("Teste de erro")


if __name__ == "__main__":
  app.run(debug=True)
```

### Com FastAPI

```python
import uvicorn
from fastapi import FastAPI
from error_dispatcher_client import FastAPIMetrics
from error_dispatcher_client.providers import KafkaProvider, EmailProvider

app = FastAPI()

kafka_provider = KafkaProvider(bootstrap_servers="localhost:9092", topic="errors")
email_provider = EmailProvider(
  smtp_server="smtp.gmail.com",
  smtp_port=587,
  username="seuemail@gmail.com",
  password="suasenha"
)

metrics = FastAPIMetrics(providers=[kafka_provider, email_provider])
metrics.init_app(app)


@app.get("/")
async def index():
  raise ValueError("Teste de erro")


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 🌟 Recursos Avançados

### Configuração de Múltiplos Provedores
Você pode usar múltiplos provedores simultaneamente, personalizando como os erros são processados.

```python
providers = [
    KafkaProvider(
      bootstrap_servers="localhost:9092",
      topic="errors"
    ),
    EmailProvider(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username="seuemail@gmail.com",
        password="suasenha"
    )
]

metrics = FlaskMetrics(providers=providers)
metrics.init_app(app)
```

### Configuração de Template de mensagem
Você pode usar da maneira que quiser os parametros a serem enviados pelos provedores, personalizando quais paramentros serao enviados, ocultando alguns por exemplo.
```python
from error_dispatcher_client import FastAPIMetrics
from error_dispatcher_client.templates import CustomTemplate
from error_dispatcher_client.providers import KafkaProvider, EmailProvider, DiscordProvider

message_template = CustomTemplate(
    {
        "app_name" : None,
        "endpoint" : None,
        "full_url" : None,
        "method" : None,
        "status_code" : None,
        "duration" : None,
        "headers" : None,
        "query_params" : None,
        #"request_body" : None,
        "client_ip" : None,
        "user_agent" : None,
        "error_details" : None,
        "error_type" : None,
        #"traceback" : None
        "timestamp" : None
    }
)

app = FastAPI()

discord_provider = DiscordProvider(
    webhook_url="https://discord.com/api/webhooks/1328369709577666633/hyiNF9Xr97YfJDnNF89GG4-e5v1sT-p-v1P32KhqWwM3F4xs3JyK1BvND8TYnA7LFj7r",
    message_template=message_template
)

metrics = FastAPIMetrics(providers=[discord_provider, kafka_provider], app_name="api-plant-manager")
metrics.init_app(app)
...

```




### Criando Provedores Personalizados
Você pode adicionar novos provedores implementando a interface `BaseProvider`:

```python
from error_dispatcher_client.providers import ErrorProvider


class CustomProvider(ErrorProvider):
  def send(self, error_data: dict):
    print("Erro recebido:", error_data)
```

---


## 📦 Estrutura do Projeto

```plaintext
error_dispatcher_client/
│
├── error_dispatcher_client/    # Código-fonte principal do pacote
│   └── templates/              # Implementações de templates de menssagem
│   │   ├── __init__.py
│   │   └── base_template.py    # Interface base para mensagens
│   └── providers/              # Implementações de provedores
│   │   ├── __init__.py
│   │   ├── base_provider.py    # Interface base para provedores
│   │   ├── kafka_provider.py   # Provedor Kafka
│   │   ├── discord_provider.py # Provedor Discord
│   │   └── email_provider.py   # Provedor de E-mail
│   ├── __init__.py
│   ├── flask_metrics.py        # Integração com Flask
│   ├── fastapi_metrics.py      # Integração com FastAPI
│   └── base_metrics.py         # Integração Base Temaplate
│
├── examples/                   # Implementacao exemplo
│   ├── fastapi_example.py      # Exemplo fastapi
│   └── test_email.py           # Exemplo flask
│
├── tests/                      # Testes unitários
│   ├── __init__.py
│   ├── test_flask.py
│   ├── test_fastapi.py
│   ├── test_kafka.py
│   └── test_email.py
│
├── README.md                   # Documentação do projeto
├── requirements.txt            # Dependencias do pacote
└── setup.py                    # Configurações do pacote
```

## 🏗️ Contribuindo
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do repositório.
2. Crie um branch para sua feature/bugfix (`git checkout -b minha-feature`).
3. Envie um pull request.

--- 
