from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
#def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
#    return 'user_{0}/{1}'.format(instance.user.id, filename)



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    public = models.BooleanField

    def __str__(self):
        return self.name


class Picture(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="gallery")
    public = models.BooleanField(default=False)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(verbose_name=('Date joined'), auto_now_add=True, blank=True)
    phone = models.TextField(blank=True)
    address = models.TextField(blank=True)
    postal_code = models.TextField(blank=True)
    city = models.TextField(blank=True)
    num_ftf = models.CharField(max_length=4)
    nb_photo = models.IntegerField(blank=True, default=0)
    site_web = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    flickr = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

