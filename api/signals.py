from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    token = reset_password_token.key

    reset_link = f"http://127.0.0.1:8000/api/v1/password_reset/confirm/?token={token}"

    subject = "🔐 Reset da tua Password"

    message = f"""
Olá,

Recebemos um pedido para redefinir a tua password.

Clica no link abaixo para continuar:

{reset_link}

Se não foste tu, ignora este email.
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email],
        fail_silently=False,
    )