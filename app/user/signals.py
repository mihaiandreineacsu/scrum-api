from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from app.settings import DEFAULT_FROM_EMAIL

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
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
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.name,
        'email': reset_password_token.user.email,
        'absolute_uri': instance.request.META.get('HTTP_ORIGIN'),
        'reset_password_url': "{}{}?token={}".format(
            instance.request.META.get('HTTP_ORIGIN'),
            '/auth/reset-password',
            reset_password_token.key)
    }

    # print(f"request origin: {instance.request.META.get('HTTP_ORIGIN')}")

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Join"),
        # message:
        email_plaintext_message,
        # from:
        DEFAULT_FROM_EMAIL,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send(fail_silently=True)
