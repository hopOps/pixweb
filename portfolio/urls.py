from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    #path('<int:id>', views.detail, name="detail"), # expected a integer from var id
    #patterns('',# ... the rest of your URLconf goes here ...) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]