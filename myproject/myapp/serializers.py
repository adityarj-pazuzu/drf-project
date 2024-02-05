from rest_framework import serializers
from rest_framework.request import Request
from myapp.models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'created_at', 'modified_at', 'author']
        read_only_fields = ['author']
        
    def create(self, validated_data):
        # Automatically set the author to the authenticated user during creation
        request = self.context.get('request')  # Access the request object
        validated_data['author'] = request.user  # Set the author
        return super().create(validated_data)

    def get_author(self, obj):
        return obj.author.username if obj.author else None
    
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['author'] = obj.author.username
        return representation