from django.contrib import admin

from .models import Profile, Category, Picture

# Register your models here.
admin.site.register(Category)
admin.site.register(Picture)
admin.site.register(Profile)

