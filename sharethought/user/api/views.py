from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from knox.views import LoginView as KnoxLoginView
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from user.api import signals
from user.api.serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    UserRequestSerializer,
)
from user.models import UserRequest

User = get_user_model()


class SignupView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = (
                "Your account is sent for verification, you will get mail of verification"
                " status"
            )
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["user"].is_verified:
            signals.post_save.disconnect(receiver=User, sender=User)
            user = serializer.validated_data["user"]
            login(request, user)
        else:
            error_message = (
                "Your account is not yet verified by admin, please wait until you"
                " get email of verification"
            )
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        return super(LoginView, self).post(request, format=None)


class UserRetrieveUpdateView(
    UserPassesTestMixin, SingleObjectMixin, RetrieveUpdateAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = [
        "id",
        "email",
        "phone_number",
        "name",
        "role",
        "is_superuser",
        "is_staff",
        "is_verified",
        "date_joined",
    ]

    def test_func(self):
        instance = self.get_object()
        if (
            instance.id == self.request.user.id
            or self.request.user.is_superuser
            or self.request.user.is_staff
        ):
            return True


class UserAccountDeactivateView(UserPassesTestMixin, SingleObjectMixin, UpdateAPIView):
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["pk"])
        if user:
            user.is_active = False
            user.save()
            message = (
                "Your account has been deactivated, you can again activate your account by "
                "sending request to admin for activating"
            )
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = "User doesn't exists"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def test_func(self):
        instance = self.get_object()
        if (
            instance.id == self.request.user.id
            or self.request.user.is_superuser
            or self.request.user.is_staff
        ):
            return True


class UserAccountActivateView(CreateAPIView):
    serializer_class = UserRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not serializer.validated_data["user"].is_active:
                serializer.save()
                message = "Account activation request has been sent to admin."
                return Response(message, status=status.HTTP_200_OK)
            elif serializer.validated_data["user"].is_active:
                message = "Your account is already activated, you can use your account."
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRequestListView(ListAPIView):
    serializer_class = UserRequestSerializer
    permission_classes = [AllowAny]
    filterset_fields = ["request"]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return UserRequest.objects.all()
        else:
            return UserRequest.objects.filter(user=self.request.user.id)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = [
        "id",
        "email",
        "phone_number",
        "name",
        "role",
        "is_superuser",
        "is_staff",
        "is_verified",
        "date_joined",
    ]


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class CustomSocialLoginView(SocialLoginView):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class GoogleLoginView(CustomSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    def get_response(self):
        self.user.is_email_verified = True
        self.user.save()
        return Response({"data": {}})

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(
            data=self.request.data, context={"request": request}
        )
        if self.serializer.is_valid(raise_exception=True):
            self.login()
            return self.get_response()
        return Response({"data": {}})
