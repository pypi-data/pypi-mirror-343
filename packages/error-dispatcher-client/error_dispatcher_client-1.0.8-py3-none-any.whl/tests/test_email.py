from error_dispatcher_client.providers import EmailProvider

def test_email_provider(mocker):
    mock_smtp = mocker.patch("smtplib.SMTP")
    provider = EmailProvider(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username="seuemail@gmail.com",
        password="suasenha"
    )
    provider.send({"error": "Teste"})
    mock_smtp().sendmail.assert_called_once()
