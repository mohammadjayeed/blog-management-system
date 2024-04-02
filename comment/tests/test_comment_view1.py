import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Blog
from comment.models import Comment
from comment.serializers import CommentPostSerializer

@pytest.mark.django_db
class TestCommentCreateViewSet:

    def test_create_comment_success(self):

        client = APIClient()
        
        user = User.objects.create_user(username='testuser', password='testpassword')

        
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)

        
        client.force_authenticate(user=user)

        
        url = f'/api/v1/blog/{blog.pk}/comment/'
        data = {'comment': 'Test Comment'}
        response = client.post(url, data, format='json')

        # Assert the response
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'status': 'success', 'message': 'comment posted.'}

        # Assert the comment is created in the database
        comment = Comment.objects.get(author=user, blog=blog)
        assert comment.comment == 'Test Comment'

    def test_create_comment_invalid_data(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')

        
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)

        # Login the user
        client.force_authenticate(user=user)

        # Send a POST request with invalid data
        url = f'/api/v1/blog/{blog.pk}/comment/' 
        data = {'comment': ''}
        response = client.post(url, data, format='json')

        # Assert the response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'status': 'error', 'message': {'comment': ['This field may not be blank.']}}

        # Assert no comment is created in the database
        assert Comment.objects.filter(author=user, blog=blog).count() == 0

    def test_create_author_already_commented(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')

        
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)

        Comment.objects.create(author=user, blog=blog, comment='Test Comment')

        
        client.force_authenticate(user=user)

        # Send a POST request to create a comment
        url = f'/api/v1/blog/{blog.pk}/comment/'
        data = {'comment': 'Another Comment'}
        response = client.post(url, data, format='json')

        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'comment_status': ['Already commented by author']}

        assert Comment.objects.filter(author=user, blog=blog).count() == 1