from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta
from .models import Blog
from django.contrib.auth.models import User


class BlogViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='admin1', password='admin1')
        self.user2 = User.objects.create_user(username='admin2', password='admin2')
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.client1.force_authenticate(user=self.user1)
        self.client2.force_authenticate(user=self.user2)

    def create_blog(self, title='Test Blog', content='Test content', author=None):
        if not author:
            author = self.user1
        return Blog.objects.create(title=title, content=content, author=author)

    def test_get_blog_list_unauthenticated(self):
        response = self.client.get(reverse('blog-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_blog_list_authenticated(self):
        self.create_blog()
        response = self.client1.get(reverse('blog-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_blog_authenticated(self):
        blog_data = {'title': 'New Test Blog', 'content': 'This is a new test blog content.'}
        response = self.client1.post(reverse('blog-list'), blog_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.get().title, 'New Test Blog')

    def test_update_blog_authenticated(self):
        blog = self.create_blog()
        updated_data = {'title': 'Updated Test Blog', 'content': 'This is an updated test blog content.'}
        response = self.client1.put(reverse('blog-detail', args=[blog.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Blog.objects.get().title, 'Updated Test Blog')

    def test_delete_blog_authenticated(self):
        blog = self.create_blog()
        response = self.client1.delete(reverse('blog-detail', args=[blog.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Blog.objects.count(), 0)

    def test_search_blog_by_title_unauthenticated(self):
        self.create_blog()
        response = self.client.get(reverse('blog-list') + '?title=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    def test_search_blog_by_author_unauthenticated(self):
        self.create_blog()
        response = self.client.get(reverse('blog-list') + f'?author={self.user1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    def test_get_blogs_by_date(self):
        blog = self.create_blog()
        response = self.client1.get(reverse('blog-by-date') + f'?date={blog.created_at.date()}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_blogs_by_date_range(self):
        blog = self.create_blog()
        start_date = blog.created_at.date() - timedelta(days=1)
        end_date = blog.created_at.date() + timedelta(days=1)
        response = self.client1.get(reverse('blog-by-date-range') +
                                    f'?start_date={start_date}&end_date={end_date}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_blogs_created_after_date(self):
        blog = self.create_blog()
        date_after = blog.created_at.date() - timedelta(days=1)
        response = self.client1.get(reverse('blog-created-after-date') + f'?date={date_after}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_blogs_created_before_date(self):
        blog = self.create_blog()
        date_before = blog.created_at.date() + timedelta(days=1)
        response = self.client1.get(reverse('blog-created-before-date') + f'?date={date_before}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_blogs_by_different_users(self):
    # Create blogs for different users
        blog_user1 = self.create_blog(author=self.user1)
        blog_user2 = self.create_blog(author=self.user2)

        # Retrieve blogs for user 1
        response_user1 = self.client1.get(reverse('blog-list') + f'?author={self.user1.id}')
        
        # Retrieve blogs for user 2
        response_user2 = self.client2.get(reverse('blog-list') + f'?author={self.user2.id}')

        # Assert that the status code is OK
        self.assertEqual(response_user1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user2.status_code, status.HTTP_200_OK)

        # Assert that each user gets only their own blog
        self.assertEqual(len(response_user1.data), 1)
        self.assertEqual(len(response_user2.data), 1)
        
        # Assert that the retrieved blogs have the correct author
        self.assertEqual(response_user1.data[0]['author'], self.user1.username)
        self.assertEqual(response_user2.data[0]['author'], self.user2.username)


    def test_update_blog_by_different_users(self):
        blog_user1 = self.create_blog(author=self.user1)
        updated_data = {'title': 'Updated Test Blog', 'content': 'This is an updated test blog content.'}
        
        response_user2 = self.client2.put(reverse('blog-detail', args=[blog_user1.id]), updated_data, format='json')
        self.assertEqual(response_user2.status_code, status.HTTP_403_FORBIDDEN)
        
        response_user1 = self.client1.put(reverse('blog-detail', args=[blog_user1.id]), updated_data, format='json')
        self.assertEqual(response_user1.status_code, status.HTTP_200_OK)
        self.assertEqual(Blog.objects.get().title, 'Updated Test Blog')
