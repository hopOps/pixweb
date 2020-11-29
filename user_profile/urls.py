from django.urls import path
from django.conf import settings

from . import views

app_name = 'user_profile'

urlpatterns = [
    path('register', views.register, name="register"),
    path('logout', views.logout_user, name="logout"),
    path('login', views.login_user, name="login"),
    path('edit_user', views.edit_user, name="edit_user"),
]
