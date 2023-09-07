from django.contrib.auth.models import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, BooleanField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from user.api.managers import CustomUserManager

ADMIN = "Admin"
AUTHOR = "Author"
USER = "User"
ACCOUNT_ACTIVATE = "Account activate request"

ROLES = ((ADMIN, "Admin"), (AUTHOR, "Author"), (USER, "User"))
REQUESTS = ((ACCOUNT_ACTIVATE, "Account activate"),)


class User(AbstractUser):

    username = None
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = EmailField(_("Email Address"), unique=True)
    phone_number = PhoneNumberField(
        _("Phone Number"), null=True, blank=True, unique=True
    )
    role = CharField(_("Signup As"), max_length=10, choices=ROLES, default=USER)
    is_verified = BooleanField(_("Is Verified"), default=False)
    raw_password = CharField(
        _("Raw Password"), max_length=10, null=True, blank=True, default="password"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse("user:detail", kwargs={"username": self.username})


class UserRequest(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_requests"
    )
    request = models.CharField(_("Request"), max_length=50, choices=REQUESTS)

    def __str__(self):
        return f"User: {self.user.email}, Request: {self.request}"
