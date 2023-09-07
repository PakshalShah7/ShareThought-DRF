from rest_framework import serializers

from thought.models import Image, Thought


class ThoughtSerializer(serializers.ModelSerializer):
    images_list = serializers.ListSerializer(
        child=serializers.ImageField(), write_only=True
    )

    class Meta:
        model = Thought
        fields = [
            "id",
            "author",
            "title",
            "images",
            "content",
            "status",
            "images_list",
            "likes",
            "is_comment_enabled",
        ]
        extra_kwargs = {"author": {"required": False}}

    def create(self, validated_data):
        thought = Thought.objects.create(
            author=self.context["request"].user,
            title=validated_data["title"],
            content=validated_data["content"],
            status=validated_data["status"],
            is_comment_enabled=validated_data["is_comment_enabled"],
        )
        images = []
        for image in validated_data["images_list"]:
            image_id = Image.objects.create(image=image)
            images.append(image_id)
        thought.images.set(images)
        return thought

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.status = validated_data.get("status", instance.status)
        instance.is_comment_enabled = validated_data.get(
            "is_comment_enabled", instance.is_comment_enabled
        )

        images = []
        for image in validated_data["images_list"]:
            image_id = Image.objects.filter(image=image)

            if image_id.exists():
                images.append(image_id.first())
            else:
                image_id = Image.objects.create(image=image)
                images.append(image_id)
        instance.images.set(images)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super(ThoughtSerializer, self).to_representation(instance)
        if representation["author"]:
            representation["author"] = instance.author.email
        return representation


class LikeSerializer(serializers.ModelSerializer):
    thought_id = serializers.IntegerField(source="id", write_only=True)

    class Meta:
        model = Thought
        fields = [
            "id",
            "author",
            "title",
            "images",
            "content",
            "status",
            "thought_id",
            "likes",
            "is_comment_enabled",
        ]
        extra_kwargs = {"author": {"required": False}, "content": {"required": False}}
