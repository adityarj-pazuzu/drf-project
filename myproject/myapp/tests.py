# your_app_name/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Blog

class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='This is a test blog content.',
            author=self.user
        )
        self.client = APIClient()

    def test_create_blog(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Test Blog',
            'content': 'This is a new test blog content.'
        }
        response = self.client.post('/blogs/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)

    def test_get_blog_list(self):
        response = self.client.get('/blogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_get_blog_detail(self):
        response = self.client.get(f'/blogs/{self.blog.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Blog')

    def test_update_blog(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Test Blog',
            'content': 'This is an updated test blog content.'
        }
        response = self.client.put(f'/blogs/{self.blog.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, 'Updated Test Blog')

    def test_delete_blog(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/blogs/{self.blog.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Blog.objects.count(), 0)
        
    def test_create_blog_unauthenticated(self):
        data = {
            'title': 'New Test Blog',
            'content': 'This is a new test blog content.'
        }
        response = self.client.post('/blogs/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Blog.objects.count(), 1)

    def test_get_blog_list_filtered_by_author(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        another_blog = Blog.objects.create(
            title='Another Test Blog',
            content='This is another test blog content.',
            author=another_user
        )
        response = self.client.get(f'/blogs/?author={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_get_blog_list_filtered_by_title(self):
        response = self.client.get(f'/blogs/?title=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_get_blog_list_filtered_by_date(self):
        response = self.client.get(f'/blogs/?created_at={self.blog.created_at.date()}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Blog')

    def test_update_blog_unauthorized(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.force_authenticate(user=another_user)
        data = {
            'title': 'Updated Test Blog',
            'content': 'This is an updated test blog content.'
        }
        response = self.client.put(f'/blogs/{self.blog.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.blog.refresh_from_db()
        self.assertNotEqual(self.blog.title, 'Updated Test Blog')

    def test_delete_blog_unauthorized(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(f'/blogs/{self.blog.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Blog.objects.count(), 1)