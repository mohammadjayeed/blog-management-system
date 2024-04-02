import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from blog.models import Blog


@pytest.mark.django_db
class TestBlogRetrieveUpdateDeleteViewSet:
    def test_retrieve_existing_blog(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        # client.force_authenticate(user=user)

        blog = Blog.objects.create(title="Test Blog", content="Test content",author=user)
        url = f"/api/v1/blog/{blog.pk}/"

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "success"
        assert response.data["results"]["title"] == "Test Blog"
        assert response.data["results"]["content"] == "Test content"

    def test_retrieve_non_existing_blog(self):
        client = APIClient()
        url = "/api/v1/blog/999/"

        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["status"] == "success"
        assert response.data["message"] == "No matching Blog post."

    def test_update_existing_blog(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)

        blog = Blog.objects.create(title="Test Blog", content="Test content", author=user)
        url = f"/api/v1/blog/{blog.pk}/"
        data = {
            "title": "Updated Blog",
            "content": "Updated content"
        }

        response = client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "success"
        assert response.data["message"] == "Blog updated successfully."

        updated_blog = Blog.objects.get(pk=blog.pk)
        assert updated_blog.title == "Updated Blog"
        assert updated_blog.content == "Updated content"

    def test_update_non_existing_blog(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)
        url = "/api/v1/blog/999/"
        data = {
            "title": "Updated Blog",
            "content": "Updated content"
        }

        response = client.put(url, data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["status"] == "success"
        assert response.data["message"] == "Sorry, we couldn't find any matching post."

    def test_update_unauthorized_blog(self):
        client1 = APIClient()
        client2 = APIClient()
        user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        client1.force_authenticate(user=user1)

        

        
        blog = Blog.objects.create(title="Test Blog", content="Test content", author = user1)

        user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        client2.force_authenticate(user=user2)

        url = f"/api/v1/blog/{blog.pk}/"

        data = {
            "title": "Updated Blog",
            "content": "Updated content"
        }

        response = client2.put(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["status"] == "error"
        assert response.data["message"] == "You do not have permission to update this post."

    def test_destroy_existing_blog(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)

        blog = Blog.objects.create(title="Test Blog", content="Test content", author=user)
        url = f"/api/v1/blog/{blog.pk}/"

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["status"] == "success"
        assert response.data["message"] == "Product deleted successfully."

        with pytest.raises(Blog.DoesNotExist):
            Blog.objects.get(pk=blog.pk)

    def test_destroy_non_existing_blog(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)
        url = "/api/v1/blog/999/"

        response = client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["status"] == "success"
        assert response.data["message"] == "Sorry, we couldn't find any matching post."

    def test_destroy_unauthorized_blog(self):
        client1 = APIClient()
        client2 = APIClient()
        user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        client1.force_authenticate(user=user1)

        blog = Blog.objects.create(title="Test Blog", content="Test content", author=user1)

        user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        client2.force_authenticate(user=user2)

        url = f"/api/v1/blog/{blog.pk}/"

        response = client2.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["status"] == "error"
        assert response.data["message"] == "You do not have permission to delete this post."
