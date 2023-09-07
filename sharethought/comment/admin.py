from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    date_hierarchy = "created"
    ordering = ["-id"]
    search_fields = [
        "user__name__icontains",
        "user__email__icontains",
        "user__phone_number__icontains",
        "thought__title__icontains",
        "thought__content__icontains",
        "parent__icontains",
        "comment__icontains",
    ]
    list_display = ["thought", "user", "comment", "parent"]
    list_per_page = 10
