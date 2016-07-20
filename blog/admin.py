from django.contrib import admin
from .models import Attachment, Category, Post


admin.site.register(Attachment)
admin.site.register(Category)
admin.site.register(Post)
