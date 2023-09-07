from django.urls import path, include
from rest_framework.routers import SimpleRouter

from thought.api.views import ThoughtView, LikeView

app_name = "thought_api"

router = SimpleRouter()
router.register("thoughts", ThoughtView, basename="thoughts")

urlpatterns = [
    path("", include(router.urls)),
    path("thought/likes/", LikeView.as_view(), name="thought_likes"),
]
