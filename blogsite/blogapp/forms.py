from django import forms

from blogapp.models import Blog

class BlogForm(forms.ModelForm):
    """
        Blog form for create and update blog
    """

    class Meta:
        model =Blog
        fields = ['title','description','post','categories']
