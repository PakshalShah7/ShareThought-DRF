from django.urls import path, include
from rest_framework.routers import SimpleRouter

from comment.api.views import CommentView

app_name = "comment_api"

router = SimpleRouter()
router.register("comments", CommentView, basename="comments")

urlpatterns = [path("", include(router.urls))]
