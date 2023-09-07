import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from user.api.views import GoogleLoginView

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("api/v1/user/", include("user.api.urls", namespace="user_api")),
    path("api/v1/thought/", include("thought.api.urls", namespace="thought_api")),
    path("api/v1/comment/", include("comment.api.urls", namespace="comment_api")),
    path(
        "api/v1/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("rest-auth/google/", GoogleLoginView.as_view(), name="google"),
    path("accounts/", include("allauth.urls")),
)

if settings.DEBUG:
    urlpatterns += [
        # Testing 404 and 500 error pages
        path("404/", TemplateView.as_view(template_name="404.html"), name="404"),
        path("500/", TemplateView.as_view(template_name="500.html"), name="500"),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
