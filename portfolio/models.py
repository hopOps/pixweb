from django.db import models


# Create your models here.
#def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
#    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    mail = models.EmailField

    def __str__(self):
        return self.first_name + " " + self.last_name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    public = models.BooleanField

    def __str__(self):
        return self.name


class Picture(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    photo = models.ImageField(upload_to="gallery")

