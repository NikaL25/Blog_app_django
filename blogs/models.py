from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='blog_photos/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment from {self.author.username} к {self.blog.title}"

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=100)  
    target_type = models.CharField(max_length=50) 
    target_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actor.username} {self.verb} your {self.target_type}"