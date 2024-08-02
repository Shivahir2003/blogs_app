from django.contrib import admin

from blogapp.models import Blog,Category,Comments,Reply

admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Reply)
