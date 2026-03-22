from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
# Create your models here.
