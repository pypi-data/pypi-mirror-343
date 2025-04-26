import smtplib
from email.mime.text import MIMEText
from .base_provider import ErrorProvider
from error_dispatcher_client.templates import TemplateBase

class EmailProvider(ErrorProvider):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str,  message_template: TemplateBase = None):
        """
        Implementa servidor SMTP
        """
        super().__init__()
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send(self, error_data: dict):
        try:
            self.message_template.update(error_data)
            error_data = self.message_template.as_dict()
            subject = f"Error Alert: {error_data['error']}"
            body = f"Details:\n\n{error_data}"

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.username
            msg["To"] = self.username

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, [self.username], msg.as_string())
        except Exception as e:
            self.logger.error(f"Erro ao enviar email: {e}")
