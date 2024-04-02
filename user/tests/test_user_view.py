import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestCreateUserView:

    def test_create_user_success(self):
        client = APIClient()

        
        url = '/api/v1/register/'
        data = {'username': 'testuser', 'email':'test@gmail.com', 'password': 'testpassword'}
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'username': 'testuser', 'email': 'test@gmail.com'}

        assert User.objects.filter(username='testuser').exists()

    def test_create_user_invalid_data(self):
        client = APIClient()

        url = '/api/v1/register/'
        data = {'username': '','email':'test@gmail.com', 'password': 'testpassword'}
        response = client.post(url, data, format='json')

        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'username': ['This field may not be blank.']}
        assert not User.objects.exists()