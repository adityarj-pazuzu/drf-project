"""apps.py"""
from django.apps import AppConfig


class MyappConfig(AppConfig):
    """Register app name"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"
