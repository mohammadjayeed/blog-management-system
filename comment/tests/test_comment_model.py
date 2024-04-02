import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from blog.models import Blog
from comment.models import Comment

@pytest.mark.django_db
class TestCommentModel:
    def test_comment_str(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)
        comment = Comment.objects.create(author=user, blog=blog, comment='Test Comment')
        assert str(comment) == 'Test Comment'

    def test_comment_attributes(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)
        comment = Comment.objects.create(author=user, blog=blog, comment='Test Comment')
        assert comment.author == user
        assert comment.blog == blog
        assert comment.comment == 'Test Comment'

    def test_comment_timestamps(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)
        comment = Comment.objects.create(author=user, blog=blog, comment='Test Comment')
        assert comment.created_at is not None
        assert comment.updated_at is not None

    def test_comment_unique_together(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)
        Comment.objects.create(author=user, blog=blog, comment='Test Comment')

        with pytest.raises(Exception):
            Comment.objects.create(author=user, blog=blog, comment='Test Comment')

    def test_comment_deletion_on_user_delete(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        blog = Blog.objects.create(title='Test Blog', content='Test Content', author=user)
        comment = Comment.objects.create(author=user, blog=blog, comment='Test Comment')

        user_id = user.id
        assert Comment.objects.filter(author_id=user_id).count() == 1

        user.delete()

        assert Comment.objects.filter(author_id=user_id).count() == 0