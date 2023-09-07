from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from rest_framework.viewsets import ModelViewSet

from comment.api.serializers import CommentSerializer
from comment.models import Comment


class CommentView(UserPassesTestMixin, SingleObjectMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def test_func(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            instance = self.get_object()
            return instance.user == self.request.user
        return True
