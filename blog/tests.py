from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post

class PostAPITests(TestCase):

    def setUp(self):
        # This runs before every test
        self.client = APIClient()

        # Create two test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )

        # Create a test post owned by user1
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            owner=self.user1
        )

    def test_get_all_posts(self):
        # Anyone can get all posts
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('✅ GET posts works!')

    def test_create_post_authenticated(self):
        # Logged in user can create a post
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print('✅ Authenticated POST works!')

    def test_create_post_unauthenticated(self):
        # Non logged in user cannot create a post
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('✅ Unauthenticated POST blocked!')

    def test_delete_own_post(self):
        # User can delete their own post
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print('✅ Owner can delete post!')

    def test_delete_other_users_post(self):
        # User cannot delete someone else's post
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print('✅ Non-owner blocked from deleting!')