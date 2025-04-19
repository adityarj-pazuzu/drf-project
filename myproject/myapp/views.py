"""
This module defines the BlogViewSet for managing Blog instances in the API.

It provides standard CRUD operations, as well as custom filtering endpoints
for querying blogs by author, specific dates, or date ranges.
"""

from datetime import datetime
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone

from .models import Blog
from .serializers import BlogSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.query_params.get("author")
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset

    @action(detail=False, methods=["get"])
    def by_date(self, request, *args, **kwargs):
        """
        Return blogs created on a specific date.
        Query Params:
            date (str): Date in 'YYYY-MM-DD' format.
        Returns:
            Response: Serialized list of blog posts from the specified date.
        """
        date_str = request.query_params.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        blogs = Blog.objects.filter(created_at__date=date)
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_date_range(self, request, *args, **kwargs):
        """
        Return blogs created within a specific date range.
        Query Params:
           start_date (str): Start date in 'YYYY-MM-DD' format.
           end_date (str): End date in 'YYYY-MM-DD' format.
        Returns:
           Response: Serialized list of blog posts in the given date range.
        """
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        blogs = Blog.objects.filter(created_at__date__range=(start_date, end_date))
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def created_after_date(self, request, *args, **kwargs):
        """
        Return blogs created after a given date
        Query Params:
            date (str): Date in 'YYYY-MM-DD' format.
        Returns:
            Response: Serialized list of blog posts created after the specified date.
        """
        date_str = request.query_params.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        blogs = Blog.objects.filter(created_at__date__gt=date)
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def created_before_date(self, request, *args, **kwargs):
        """
        Return blogs created before a given date.
        Query Params:
            date (str): Date in 'YYYY-MM-DD' format.
        Returns:
            Response: Serialized list of blog posts created before the specified date
        """
        date_str = request.query_params.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        blogs = Blog.objects.filter(created_at__date__lt=date)
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Update an existing blog post if the authenticated user is the author.
        Raises:
            PermissionDenied: If the requesting user is not the blog's author.
        Returns:
            Response: Success message and updated blog data.
        """
        instance = serializer.instance
        # Check if the user making the request is the author of the blog
        if self.request.user != instance.author:
            raise PermissionDenied("You do not have permission to update this blog.")

        instance = serializer.save(modified_at=timezone.now())
        return Response(
            {
                "message": f'Blog "{instance.title}" updated successfully!',
                "data": self.get_serializer(instance).data,
            }
        )

    def perform_destroy(self, instance):
        """
        Delete a blog post and return a custom message.
        Args:
            instance (Blog): The blog post instance to be deleted.
        Returns:
            Response: Success message with 204 No Content status.
        """
        instance_title = instance.title
        instance.delete()
        response_message = f'Blog "{instance_title}" deleted successfully!'
        return Response(
            {"message": response_message}, status=status.HTTP_204_NO_CONTENT
        )
