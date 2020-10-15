from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('list', views.list.as_view(), name="list"),
    path('display', views.display, name="display"),
    path('<int:pk>', views.detail.as_view(), name="detail"),
    path('', views.index, name="index"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static('/', document_root=settings.MEDIA_ROOT)

#patterns('',# ... the rest of your URLconf goes here ...) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)