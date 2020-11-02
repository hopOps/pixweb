from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('list', views.list.as_view(), name="list"),
    path('gallery', views.gallery, name="gallery"),
    path('mygallery', views.mygallery, name="mygallery"),
    path('register', views.register, name="register"),
    path('logout', views.logout_user, name="logout"),
    path('login', views.login_user, name="login"),
    path('edit_user', views.edit_user, name="edit_user"),
    path('<int:pk>', views.picture.as_view(), name="picture"),
    path('', views.index, name="index"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static('/', document_root=settings.MEDIA_ROOT)

#patterns('',# ... the rest of your URLconf goes here ...) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)