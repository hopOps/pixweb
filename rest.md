## Doc references

    https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react

## To get json rest data

http://127.0.0.1:8000/portfolio/api/pictures/

## To install modules

    pip install django-cors-headers
    pip install djangorestframework


## To declare and init modules

Add 'portfolio' apps ins settings.py :

    INSTALLED_APPS = [
    ...
    'corsheaders',  # restjson
    'rest_framework',  # restjson
    ]
    
Add 'coresherders' middlewares in settings.py :

    MIDDLEWARE = [
    ...
    ''corsheaders.middleware.CorsMiddleware',',
    ]    
    
Edit allowed host to access for API in settings.py :
    CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'https://127.0.0.1:8000'
 )
 
 
 ## Create the serializers.py to ref in model data
 
    # portfolio/serializers.py

    from rest_framework import serializers
    from .models import Picture, Category


    class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('id', 'name', 'user', 'category', 'description', 'pub_date', 'photo', 'public')

## Create the view in portfolio/view.py

    # Rest
    from rest_framework import viewsets
    from .serializers import PictureSerializer, CategorySerializer

    class pictures(viewsets.ModelViewSet):
        serializer_class = PictureSerializer
        queryset = Picture.objects.all()



## Map the URLS in portfolio/urls.py

    from rest_framework import routers

    from . import views

    router = routers.DefaultRouter()
    router.register(r'pictures', views.pictures, 'pictures')
    
    
    urlpatterns = [
        path('api/', include(router.urls)),
    ]