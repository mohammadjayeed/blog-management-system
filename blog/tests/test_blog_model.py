import pytest
from django.contrib.auth.models import User
from blog.models import Blog

@pytest.mark.django_db
class TestBlogModel:
    def test_blog_str(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)
        assert str(blog) == 'Test Blog'

    def test_blog_attributes(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)
        assert blog.title == 'Test Blog'
        assert blog.content == 'Test Content'
        assert blog.author == user

    def test_blog_timestamps(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)
        assert blog.created_at is not None
        assert blog.updated_at is not None

    def test_blog_deletion_on_user_delete(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)

        user_id = user.id
        assert Blog.objects.filter(author_id=user_id).count() == 1
        
        user.delete()
        
        assert Blog.objects.filter(author_id=user_id).count() == 0