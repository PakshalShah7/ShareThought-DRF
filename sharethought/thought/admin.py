from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from thought.models import Image, Thought


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    date_hierarchy = "created"
    ordering = ["-id"]
    list_display = ["thought_image"]
    list_per_page = 10

    def thought_image(self, obj):
        return format_html(
            "<img src='{}' width='150' height='100'/>".format(obj.image.url)
        )

    thought_image.short_description = "Thought Image"


@admin.register(Thought)
class ThoughtAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    date_hierarchy = "created"
    ordering = ["-id"]
    search_fields = [
        "author__name__icontains",
        "author__email__icontains",
        "author__phone_number__icontains",
        "title__icontains",
        "content__icontains",
    ]
    list_display = ["author", "title", "status", "thought_images"]
    list_filter = ["status"]
    list_per_page = 10

    def thought_images(self, obj):
        html = "<img src='{}' width='150' height='100'/>"
        return format_html(
            "".join(html.format(image.image.url) for image in obj.images.all())
        )

    thought_images.short_description = "Thought Images"
