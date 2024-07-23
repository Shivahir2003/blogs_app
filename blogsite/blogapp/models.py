from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Blog(TimeStampedModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=120)
    description=models.TextField(blank=True, null=True)
    post=RichTextField()
    categories = models.OneToOneField("Category",on_delete=models.RESTRICT)

    def __str__(self):
        return self.title


class Comments(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.blog.title


class Reply(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE)
    reply= models.TextField()

    def __str__(self):
        return self.reply
