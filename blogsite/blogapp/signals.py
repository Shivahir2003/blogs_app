from django.dispatch import receiver
from django.core.signals import request_finished
from django.db.models.signals import post_save,pre_save

from blogapp.utils import send_email
from blogapp.models import Comments,Reply

@receiver(pre_save ,sender=Reply)
def send_reply_mail(sender,instance,**kwargs):
        import pdb; pdb.set_trace()
        # subject= "{user} is replyed on your comment {comment}"
        # message = "{user} is replyed : {reply}"
        # send_email(subject,message,request.user)
        print("user replyed someone")
        print(sender,instance,kwargs)

@receiver(post_save , sender=Comments)
def send_comment_mail(sender,instance,**kwargs):
        import pdb; pdb.set_trace()
        print("user commented someone")
        print(sender,instance,kwargs)

