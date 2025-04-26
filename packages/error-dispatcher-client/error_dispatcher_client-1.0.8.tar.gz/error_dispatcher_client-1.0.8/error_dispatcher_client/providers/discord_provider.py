import json
from .base_provider import ErrorProvider
from discord_webhook import DiscordWebhook, DiscordEmbed
from error_dispatcher_client.templates import TemplateBase

class DiscordProvider(ErrorProvider):
    def __init__(self, webhook_url: str, username: str = "Error Dispatch", message_template: TemplateBase = None):
        """
        Inicializa o provedor do Discord.
        """
        super().__init__(message_template=message_template)
        self.webhook_url = webhook_url
        self.username = username

    def send(self, error_data: dict):
        """
        Envia a mensagem de erro para o Webhook do Discord.
        """
        try:
            self.message_template.update(error_data)
            sanitized_error_data = {
                key: str(value) if not isinstance(value, (str, int, float, bool, type(None), list, dict)) else value
                for key, value in self.message_template.as_dict().items()
            }
            error_details = json.dumps(sanitized_error_data, indent=2)

            webhook = DiscordWebhook(
                url=self.webhook_url,
                username=self.username,
            )

            embed = DiscordEmbed(
                title=f"⚠️ {error_data.get('app_name')} ⚠️ ".lower(),
                description="Um erro foi encontrado nessa api.",
                color="FF0000"
            )
            embed.add_embed_field(name="Mensagem de Erro", value=f"```{error_data.get('error_type')}```", inline=False)
            embed.add_embed_field(name="Detalhes do Erro", value=f"```json\n{error_details}\n```", inline=False)

            webhook.add_embed(embed)

            webhook.execute()
        except Exception as e:
            print(f"Erro ao enviar mensagem para o Discord: {e}")
