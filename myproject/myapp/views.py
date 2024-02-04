from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Blog
from .serializers import BlogSerializer

class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save(modified_at=timezone.now())
        updated_blog = self.retrieve(request=self.request, pk=instance.pk)
        return Response({'message': f'Blog "{instance.title}" updated successfully!', 'data': updated_blog.data})

    def perform_destroy(self, instance):
        instance.delete()
        response_message = f'Blog "{instance.title}" deleted successfully!'
        return Response({'message': response_message}, status=204)