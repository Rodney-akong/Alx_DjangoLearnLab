from django.db import models
from django.contrib.auth.models import User   # to connect posts to users

class Post(models.Model):
    title = models.CharField(max_length=200)  # short text, limited to 200 chars
    content = models.TextField()              # long text (blog content)
    published_date = models.DateTimeField(auto_now_add=True)  # auto-fill current time
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    # one user can have many posts. If user is deleted, posts also deleted.

    def __str__(self):
        return self.title   # makes posts show as their title in admin
