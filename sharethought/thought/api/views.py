from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from thought.api.permissions import ThoughtPermissions
from thought.api.serializers import ThoughtSerializer, LikeSerializer
from thought.models import Thought


class ThoughtView(UserPassesTestMixin, SingleObjectMixin, ModelViewSet):
    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer
    permission_classes = [IsAuthenticated, ThoughtPermissions]
    filterset_fields = ["author", "status"]

    def test_func(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            instance = self.get_object()
            return instance.author == self.request.user
        return True


class LikeView(GenericAPIView):
    queryset = Thought.objects.all()
    serializer_class = LikeSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            thought = Thought.objects.get(id=request.data["thought_id"])
            user = self.request.user
            likes = thought.likes.all()
            if not likes or user not in likes:
                thought.likes.add(user)
            else:
                thought.likes.remove(user)
            return Response("Your response is saved", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
