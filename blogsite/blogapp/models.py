from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from model_utils.models import TimeStampedModel

from ckeditor.fields import RichTextField
from blogapp.utils import send_email


class Category(models.Model):
    """
        Blog category model
        
        Extends:
            TimeStampedModel
        
        create Category for blog
    """
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name


class Blog(TimeStampedModel):
    """
        Blog Model
        
        Extends:
            TimeStampedModel
        
        for creating Blog post
    """
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=120)
    description=models.TextField(blank=True, null=True)
    post=RichTextField()
    categories = models.ForeignKey(Category,on_delete=models.RESTRICT)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-created']

    @property
    def comments(self):
        """
            getting all comment for blog
        """
        return self.comments_set.all()


class Comments(TimeStampedModel):
    """
        Comment Model for blog
        
        Extends:
            TimeStampedModel
        
        creating comments for blog
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment

    class Meta:
        ordering=['-created']

    @property
    def reply(self):
        """
            for getting all replies for comment
        """
        return self.reply_set.all()


class Reply(TimeStampedModel):
    """
        Reply model for comment
        
        Extends:
            TimeStampedModel
        
        for creating reply for comment
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE)
    reply= models.TextField()

    def __str__(self):
        return self.reply

    class Meta:
        ordering=['-created']


@receiver(post_save , sender=Comments)
def send_comment_mail(instance,**kwargs):
    """
        Send mail for comment on post save
        
        Arguments:
            instance
        
        send mail to blog user for commenting on blog post created by user
    """
    if instance.user != instance.blog.user:
        subject= f'A New comment on the post {instance.blog.title}'
        html_content = render_to_string('email_templates/user_comments_email.html',{'instance':instance})
        text_content = strip_tags(html_content)
        send_email(subject,html_content,text_content,instance.blog.user)

@receiver(post_save ,sender=Reply)
def send_reply_mail(instance,**kwargs):
    """
        Send mail for reply on post save
        
        Arguments:
            instance
        
        sending mail to user for replying on comment created by user
    """
    if instance.user != instance.comment.user :
        subject= f'Reply to your comment on {instance.comment.blog.title}'
        html_content = render_to_string('email_templates/user_reply_email.html',{'instance':instance})
        text_content = strip_tags(html_content)
        send_email(subject,html_content,text_content,instance.comment.user)
