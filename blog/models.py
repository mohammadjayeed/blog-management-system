from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
   
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # slug = models.SlugField(max_length=150, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
