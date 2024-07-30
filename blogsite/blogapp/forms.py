from django import forms

from blogapp.models import Blog

class BlogForm(forms.ModelForm):
    
    class Meta:
        model =Blog
        fields = ['title','description','post','categories']