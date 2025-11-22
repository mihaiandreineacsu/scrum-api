from typing import Any

from django.core.mail import EmailMultiAlternatives
from django.dispatch import Signal, receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.views import ResetPasswordRequestToken

from app.settings import DEFAULT_FROM_EMAIL


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender: Signal,
    instance: ResetPasswordRequestToken,
    reset_password_token: ResetPasswordToken,
    *args: Any,
    **kwargs: Any,
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context: dict[str, Any] = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.name,
        "email": reset_password_token.user.email,
        "absolute_uri": instance.request.META.get("HTTP_ORIGIN"),
        "reset_password_url": f"{instance.request.META.get('HTTP_ORIGIN')}/auth/reset-password?token={reset_password_token.key}",
    }

    # render email text
    email_html_message = render_to_string("email/user_reset_password.html", context)
    email_plaintext_message = render_to_string("email/user_reset_password.txt", context)

    msg = EmailMultiAlternatives(
        "Password Reset for Join",
        email_plaintext_message,
        DEFAULT_FROM_EMAIL,
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    # TODO: add logging, set fail_silently=False try except that will raise OSError/smtplib.SMTPException
    _ = msg.send(fail_silently=True)
