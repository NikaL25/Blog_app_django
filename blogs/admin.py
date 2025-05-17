from django.contrib import admin
from .models import Blog, Notification,Comment
# Register your models here.

admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(Notification)
