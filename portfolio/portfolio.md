### Resize Image

Installation

    pip install django-resized


Configuration in settings.py

    DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
    DJANGORESIZED_DEFAULT_QUALITY = 75
    DJANGORESIZED_DEFAULT_KEEP_META = True
    DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
    DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
    DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

Usage

    from django_resized import ResizedImageField

    class MyModel(models.Model):
        ...
        image1 = ResizedImageField(size=[500, 300], upload_to='whatever')
        image2 = ResizedImageField(size=[100, 100], crop=['top', 'left'], upload_to='whatever')
        image3 = ResizedImageField(size=[100, 100], crop=['middle', 'center'], upload_to='whatever')
        image4 = ResizedImageField(size=[500, 300], quality=75, upload_to='whatever')
        image5 = ResizedImageField(size=[500, 300], upload_to='whatever', force_format='PNG')