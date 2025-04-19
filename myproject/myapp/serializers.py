"""
This module contains the serializers for the Blog model in the `myapp` application.
It defines a BlogSerializer class that handles serialization, deserialization, and custom logic
for the Blog objects in the Django REST Framework API.
"""

from rest_framework import serializers
from myapp.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for the Blog model.
    Convert Blog model instances to JSON format and vice versa.
    Automatically assign the authenticated user as the author when creating a blog post
    Ensures that the 'author' field is read-only on both serialization and deserialization.
    """

    class Meta:
        """
        Defines the model to be serialized and the fields to include in the serialization process.
        """

        model = Blog
        fields = ["id", "title", "content", "created_at", "modified_at", "author"]
        read_only_fields = ["author"]

    def create(self, validated_data):
        """
        Override the default `create` method.
        Automatically sets the `author` field to the currently authenticated user
        """
        request = self.context.get("request")  # Access the request object
        validated_data["author"] = request.user  # Set the author
        return super().create(validated_data)

    def get_author(self, obj):
        """
        Retrieve the username of the author for a given blog post
        """
        return obj.author.username if obj.author else None

    def to_representation(self, obj):
        """
        Customize the representation of the Blog instance
        """
        representation = super().to_representation(obj)
        representation["author"] = obj.author.username
        return representation
