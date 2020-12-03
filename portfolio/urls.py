from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers

from . import views

app_name = 'portfolio'

router = routers.DefaultRouter()
router.register(r'pictures', views.pictures, 'pictures')


urlpatterns = [
    path('list', views.list.as_view(), name="list"),
    path('gallery', views.gallery, name="gallery"),
    path('galleryv2', views.galleryv2, name="galleryv2"),
    path('mygallery', views.mygallery, name="mygallery"),
    path('<int:pk>', views.picture.as_view(), name="picture"),
    path('carousel/<int:picture_id>', views.carousel, name="carousel"),
    path('carouselv2/<int:picture_id>', views.carouselv2, name="carouselv2"),
    path('upload_image', views.upload_picture, name="upload_image"),
    path('test', views.get_photo, name="get_photo"),
 #   path('api/all_picture', views.all_picture, name="api_all_picture"),
    path('api/', include(router.urls)),
    path('', views.index, name="index"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static('/', document_root=settings.MEDIA_ROOT)
