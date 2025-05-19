from django.contrib import admin
from django.contrib import admin

from .models import BlogRecord


@admin.register(BlogRecord)
class BlogRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "is_published")
    # list_filter = ("category",)
    search_fields = (
        "title",
        "created_at",
    )

