from django.contrib.auth import get_user_model
from django.core.mail import send_mail, mail_admins
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from sharethought.settings.base import EMAIL_HOST_USER
from user.models import UserRequest

User = get_user_model()


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    email_plaintext_message = "{}?token={}".format(
        reverse("password_reset:reset-password-request"), reset_password_token.key
    )
    send_mail(
        "Password Reset for {title}".format(title="ShareThought"),
        email_plaintext_message,
        EMAIL_HOST_USER,
        [reset_password_token.user.email],
    )


@receiver(post_save, sender=User)
def send_account_verification_mail(instance, created, *args, **kwargs):
    if instance and created and not instance.is_verified:
        mail_admins(
            subject="Account Verification Request",
            message="New account has been registered with email "
            + instance.email
            + ", to verify visit site.",
            fail_silently=True,
        )
    return instance


@receiver(pre_save, sender=User)
def send_confirmation_of_account_verification_mail(instance, *args, **kwargs):
    obj = User.objects.filter(pk=instance.pk).first()
    if obj and (not obj.is_verified and instance.is_verified):
        send_mail(
            subject="Confirmation of Account Verification",
            message="Your account has been verified, you can log in now using given below"
            " credentials"
            + " Your username "
            + instance.email
            + " and your password "
            + instance.raw_password,
            from_email=EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=True,
        )
    return instance


@receiver(post_save, sender=UserRequest)
def send_account_activation_mail(instance, created, *args, **kwargs):
    if instance and created and not instance.user.is_active:
        mail_admins(
            subject="Account Activation Request",
            message="Account with email "
            + instance.user.email
            + " wants to activate account.",
            fail_silently=True,
        )
        send_mail(
            subject="Account Activation Request Received",
            message="Your request has been sent to admin, you will get mail when request will"
            " approved.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[instance.user.email],
            fail_silently=True,
        )
    return instance


@receiver(pre_save, sender=User)
def send_confirmation_of_account_activation_mail(instance, *args, **kwargs):
    obj = UserRequest.objects.filter(user=instance.pk).first()
    if obj and (not obj.user.is_active and instance.is_active):
        send_mail(
            subject="Confirmation of Account Activation",
            message="Your account has been activated, you can log in now using email "
            + instance.email,
            from_email=EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=True,
        )
    return instance
