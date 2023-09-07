from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportModelAdmin

from user.models import UserRequest

User = get_user_model()
admin.site.site_header = "ShareThought"


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    date_hierarchy = "date_joined"
    ordering = ["-id"]
    search_fields = ["name", "email", "phone_number"]
    list_display = ["email", "name", "phone_number", "role", "is_verified"]
    list_filter = ["is_superuser", "is_staff", "is_active", "is_verified", "role"]
    list_editable = ["is_verified"]
    list_per_page = 10


@admin.register(UserRequest)
class UserRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    date_hierarchy = "created"
    ordering = ["-id"]
    search_fields = ["user__name", "user__email", "user__phone_number"]
    list_display = ["user", "request"]
    list_filter = ["request"]
    list_per_page = 10
