from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from .models import Blog

class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

    def test_create_blog_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Test Blog',
            'content': 'This is a new test blog content.'
        }
        response = self.client.post('/api/blogs/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.get().author, self.user)

    def test_create_blog_unauthenticated(self):
        data = {
            'title': 'New Test Blog',
            'content': 'This is a new test blog content.'
        }
        response = self.client.post('/api/blogs/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Blog.objects.count(), 0)

    def test_get_blog_list_authenticated(self):
        Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/blogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_get_blog_list_unauthenticated(self):
        Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        response = self.client.get('/api/blogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_get_blog_detail_authenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/blogs/{blog.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Blog')

    def test_get_blog_detail_unauthenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        response = self.client.get(f'/api/blogs/{blog.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Blog')

    def test_update_blog_authenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Test Blog',
            'content': 'This is an updated test blog content.'
        }
        response = self.client.put(f'/api/blogs/{blog.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog.refresh_from_db()
        self.assertEqual(blog.title, 'Updated Test Blog')

    def test_update_blog_unauthenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        data = {
            'title': 'Updated Test Blog',
            'content': 'This is an updated test blog content.'
        }
        response = self.client.put(f'/api/blogs/{blog.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        blog.refresh_from_db()
        self.assertEqual(blog.title, 'Test Blog')

    def test_delete_blog_authenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/blogs/{blog.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Blog.objects.count(), 0)

    def test_delete_blog_unauthenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        response = self.client.delete(f'/api/blogs/{blog.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Blog.objects.count(), 1)

    def test_search_blog_by_title_authenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/blogs/?title=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_search_blog_by_title_unauthenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        response = self.client.get(f'/api/blogs/?title=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_search_blog_by_author_authenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/blogs/?author={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_search_blog_by_author_unauthenticated(self):
        blog = Blog.objects.create(title='Test Blog', content='This is a test blog content.', author=self.user)
        response = self.client.get(f'/api/blogs/?author={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')
