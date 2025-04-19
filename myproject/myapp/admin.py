"""admin.py"""
from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Admin interface fields"""

    list_display = ("title", "author", "created_at", "modified_at")
    search_fields = ("title", "author__username")
    list_filter = ("created_at", "modified_at")
    date_hierarchy = "created_at"
