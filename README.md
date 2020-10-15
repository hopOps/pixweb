# Django start Apps

## Install Django

    pip install Django
    pip install Pillow


## Launch web server

    python manage.py runserver


## Create Projects and Applications
    django-admin startproject hopops
    cd hopops
    python manage.py startapp portfolio

Add 'portfolio' apps ins settings.py :

    INSTALLED_APPS = [
    ...
    'portfolio',
    ]    
    
## Prepare Database
    python manage.py showmigrations
    python manage.py migrate
    python manage.py dbshell
  
## Redirect urls in Apps Portfolio

Create portfolio/urls.py and add this:
   
    from django.urls import path
    from . import views

    urlpatterns = [
    ]


Modify urls.py file from project to add portfolio URLs:

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('portfolio/', include('portfolio.urls')),
    ]

## Change STATIC folders location

Modify settings.py to change STATIC param

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'root')
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

Modify settings.py to change Media param (to check for production)

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/portfolio/'

Create folders from hopops folder:

* static/
* media/

Launch "collectstatic" command:

    python manage.py collectstatic

## Create Portfolio Model

Change portfolio models.py file

Create Migration files and migrate to database:

    python manage.py makemigrations
    python manage.py mgrate


## Manage applications

Create superuser

    python manage.py createsuperuser

Add theses entries on portfolio/admin.py files:

    from .models import Author, Category, Picture
    
    admin.site.register(Author)
    admin.site.register(Category)
    admin.site.register(Picture)