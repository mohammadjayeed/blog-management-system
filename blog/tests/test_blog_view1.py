import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Blog

@pytest.mark.django_db
class TestBlogCreateViewSet:
    def test_create_blog(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)

        data = {
            'title': 'Test Blog',
            'content': 'Test Content',
        }

        response = client.post('/api/v1/blog/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'success'
        assert response.data['message'] == 'blog post created.'
        assert 'id' in response.data

        blog = Blog.objects.get(id=response.data['id'])
        assert blog.title == 'Test Blog'
        assert blog.content == 'Test Content'
        assert blog.author == user

    def test_create_blog_invalid_data(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)

        data = {
            'title': '',  
            'content': 'Test Content'
        }

        response = client.post('/api/v1/blog/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert 'title' in response.data['message']

    def test_list_blogs(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)

        Blog.objects.create(title='Blog 1', content='Content 1', author=user)
        Blog.objects.create(title='Blog 2', content='Content 2', author=user)

        response = client.get('/api/v1/blog/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert 'results' in response.data
        assert len(response.data['results']) == 2

    def test_list_my_blogs(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)

        Blog.objects.create(title='Blog 1', content='Content 1', author=user)
        Blog.objects.create(title='Blog 2', content='Content 2', author=user)

        response = client.get('/api/v1/blog/me/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert 'results' in response.data
        assert len(response.data['results']) == 2

        
        all_authors_match = True
        for blog in response.data['results']: 
            if blog['author_name'] != user.username: 
                all_authors_match = False
        assert all_authors_match