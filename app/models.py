from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, )
    body = models.TextField()
    tags = TaggableManager()
    date_create = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.title


class About(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, )
    body = models.TextField()

    def str(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, )
    body = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.title
