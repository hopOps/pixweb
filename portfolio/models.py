from django.db import models

from django.contrib.auth.models import User

import os
from datetime import datetime
from django_resized import ResizedImageField

# Create your models here.


def photo_path(instance, filename):
    basefilename, file_extension=os.path.splitext(filename)
    now = datetime.now()
    strdate = now.strftime("%d-%m-%y-%f")
    return 'gallery/{username}/{strdate}{ext}'.format(username=instance.user.username, strdate=strdate, ext=file_extension)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    public = models.BooleanField

    def __str__(self):
        return self.name


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)
    photo = ResizedImageField(size=[1920, 1080], upload_to=photo_path)
    public = models.BooleanField(default=False)


