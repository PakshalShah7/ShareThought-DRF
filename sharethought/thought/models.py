from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel

User = get_user_model()


class Image(TimeStampedModel):
    image = models.ImageField(upload_to="thought_images/")


class Thought(ActivatorModel, TimeStampedModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_thoughts"
    )
    title = models.CharField(max_length=50, null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    content = models.TextField(max_length=300)
    likes = models.ManyToManyField(User, blank=True)
    is_comment_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.author.email
