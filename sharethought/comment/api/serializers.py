from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "thought", "parent", "comment"]
        extra_kwargs = {"user": {"required": False}}

    def create(self, validated_data):
        if validated_data["thought"].is_comment_enabled:
            comment = Comment.objects.create(
                user=self.context["request"].user,
                thought=validated_data["thought"],
                parent=validated_data.get("parent"),
                comment=validated_data["comment"],
            )
            return comment
        else:
            raise serializers.ValidationError(
                {"comment_disabled": "Commenting in this thought is disabled"}
            )

    def to_representation(self, instance):
        representation = super(CommentSerializer, self).to_representation(instance)
        if representation["user"]:
            representation["user"] = instance.user.email
        return representation
