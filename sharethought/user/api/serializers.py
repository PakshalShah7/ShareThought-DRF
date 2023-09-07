from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import UserRequest

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "phone_number", "role"]

        extra_kwargs = {"url": {"view_name": "user_api:user-detail"}}

    def create(self, validated_data):
        if validated_data["role"] == "Admin":
            user = User.objects.create_superuser(
                email=validated_data["email"],
                name=validated_data["name"],
                phone_number=validated_data["phone_number"],
                role=validated_data["role"],
            )
        else:
            user = User.objects.create_user(
                email=validated_data["email"],
                name=validated_data["name"],
                phone_number=validated_data["phone_number"],
                role=validated_data["role"],
            )
        user.save()
        return validated_data


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_new_password"]

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = ["user", "request"]
