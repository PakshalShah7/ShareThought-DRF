from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

from thought.models import Thought

User = get_user_model()


class Comment(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    thought = models.ForeignKey(
        Thought, on_delete=models.CASCADE, related_name="thought_comments"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="parent_comment",
    )
    comment = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.comment
