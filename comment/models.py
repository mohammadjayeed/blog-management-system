from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, related_name = 'comments')
    comment = models.TextField(max_length = 250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('author', 'blog')

    def __str__(self):
        return self.comment