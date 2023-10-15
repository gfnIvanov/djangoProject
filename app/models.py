from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body = models.TextField()
    tags = models.CharField(max_length=450)
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_create']

    def __str__(self):
        return self.title


class About(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.post)
