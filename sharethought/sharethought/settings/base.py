"""
Django's settings for a sharethought project.
"""
from datetime import timedelta
from os.path import abspath, basename, dirname, join, normpath
from sys import path

import environ
from django.urls import reverse_lazy

# PATH CONFIGURATION
BASE_DIR = dirname(dirname(__file__) + "../../../")

# Absolute filesystem path to the config directory:

CONFIG_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the project directory:
PROJECT_ROOT = dirname(CONFIG_ROOT)

env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(env_file=join(PROJECT_ROOT, ".env"))

# Absolute filesystem path to the django repo directory:
DJANGO_ROOT = dirname(PROJECT_ROOT)

# Project name:
PROJECT_NAME = basename(PROJECT_ROOT).capitalize()

# Project folder:
PROJECT_FOLDER = basename(PROJECT_ROOT)

# Project domain:
PROJECT_DOMAIN = "%s.com" % PROJECT_NAME.lower()

# Add our project to our pythonpath, this way we don"t need to type our project
# name in our dotted import paths:
path.append(CONFIG_ROOT)
# END PATH CONFIGURATION

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# DEBUG CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = STAGING = env.bool("DJANGO_DEBUG", False)
# END DEBUG CONFIGURATION

ADMINS = (("""Pakshal Shah""", "pakshal.shah@trootech.com"),)

MANAGERS = ADMINS

ADMIN_URL = env.str("DJANGO_ADMIN_URL", "admin")

DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="mysql://root:root@localhost:3306/sharethought"
    )
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)
DATABASES["default"]["OPTIONS"] = {
    "init_command": "SET default_storage_engine=InnoDB",
    "charset": "utf8mb4",
    "use_unicode": True,
}

EMAIL_BACKEND = env.str("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env.str("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "pakshal.shah@trootech.com")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "oCBs#@123")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", True)
EMAIL_PORT = env.int("EMAIL_PORT", 587)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment, this must be set to your system time zone.
TIME_ZONE = "Asia/Kuwait"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = normpath(join(PROJECT_ROOT, "media"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = normpath(join(PROJECT_ROOT, "assets"))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
    normpath(join(PROJECT_ROOT, "static")),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Make this unique and don"t share it with anybody.
SECRET_KEY = env("DJANGO_SECRET_KEY", default="")

# List of callables that know how to import templates from various sources.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (normpath(join(PROJECT_ROOT, "templates")),),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "django.template.context_processors.static",
            ]
        },
    },
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sharethought.urls"

# Python dotted a path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "sharethought.wsgi.application"

INSTALLED_APPS = [
    "user.apps.UsersConfig",
    "jazzmin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "rest_framework",
    "rest_framework.authtoken",
    "knox",
    "django_rest_passwordreset",
    "django_extensions",
    "django_filters",
    "import_export",
    "rest_auth",
    "rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "compressor",
    "phonenumbers",
    "phonenumber_field",
    "thought",
    "comment",
]

AUTH_USER_MODEL = "user.User"
LOGIN_URL = reverse_lazy("user_api:login")
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = reverse_lazy("user_api:login")

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOCALE_PATHS = (normpath(join(PROJECT_ROOT, "locale")),)

# Test double gettext function
gettext = lambda s: s  # noqa

LANGUAGES = [
    ("en", gettext("en")),
]

# Analytics
GOOGLE_ANALYTICS = env.str("GOOGLE_ANALYTICS", default="")

CACHE_ENGINES = {
    "dummy": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

CACHES = {"default": CACHE_ENGINES[env.str("CACHE", default="dummy")]}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["knox.auth.TokenAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(hours=10),
    "USER_SERIALIZER": "user.api.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": None,
    "AUTO_REFRESH": False,
}

SENTRY_DSN = env.str("SENTRY_DSN", "")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "331944935750-qd29pi876372ingno3qbcbmp0g1q6jfk.apps.googleusercontent.com",
            "secret": "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",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

JAZZMIN_SETTINGS = {
    "site_title": "SHARETHOUGHT",
    "welcome_sign": "WELCOME TO SHARETHOUGHT",
    "copyright": "Sharethought",
    "search_model": ["user.User", "thought.Thought"],
    "topmenu_links": [{"model": "user.User"}, {"model": "thought.Thought"}],
    "icons": {
        "account.EmailAddress": "fas fa-at",
        "rest_framework.authtoken.Token": "fas fa-key",
        "auth.Group": "fas fa-users",
        "comment.Comment": "fas fa-comments",
        "django_rest_passwordreset.ResetPasswordToken": "fas fa-key",
        "knox.AuthToken": "fas fa-key",
        "sites.Site": "fas fa-globe",
        "socialaccount.SocialAccount": "fas fa-user-circle",
        "socialaccount.SocialToken": "fas fa-key",
        "socialaccount.SocialApp": "fab fa-adn",
        "thought.Image": "fas fa-images",
        "thought.Thought": "fas fa-images",
        "user.UserRequest": "fas fa-portrait",
        "user.User": "fas fa-users",
    },
    "show_ui_builder": True,
}

