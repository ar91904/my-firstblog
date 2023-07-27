from django.conf import settings
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=250)
    text1 = models.CharField(max_length=250, default='')
    text2 = models.CharField(max_length=250, default='')
    text3 = models.CharField(max_length=250, default='')
    published_date = models.DateTimeField(default=timezone.now().strftime(("%d.%m.%Y %H:%M")))
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    tags = TaggableManager()

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete = models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
