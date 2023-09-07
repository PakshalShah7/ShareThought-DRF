from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "user"
    verbose_name = _("Users")

    def ready(self):
        from .api import signals  # noqa
