from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
#from django.http import HttpResponse, HttpResponseNotFound, request, response
from django.views import generic, View
from django.core.exceptions import ViewDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

from .models import Picture
# Create your views here.


class picture(generic.DetailView):
    model = Picture
    template_name = 'portfolio/picture.html'


class list(generic.ListView):
    template_name = 'portfolio/list.html'
    context_object_name = 'latest_picture_list'

    def get_queryset(self):
        """Return the last five published pictures."""
        return Picture.objects.all()


def gallery(request):
    all_picture = Picture.objects.all()
    paginator = Paginator(all_picture, 5)
    pages = request.GET.get('page', 1)
    #messages.warning(request, "This page will list all the picture", extra_tags='alert')
    try:
        all_picture = paginator.page(pages)
    except PageNotAnInteger:
        all_picture = paginator.page(1)
    return render(request, 'portfolio/gallery.html', {'all_picture': all_picture})


def index(request):
    return render(request, "portfolio/index.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if(username == ""):
            return HttpResponse("No Username!")
        if (password == ""):
            return HttpResponse("No password!")
        user = authenticate(username=username, password=password)
        if(user is None):
            return HttpResponse("Unauthorized!")
        else:
            login(request, user)
            return redirect('portfolio/')
    return render(request, 'portfolio/login.html')


def logout_user(request):
    logout(request)
    return HttpResponse("Successfully logged out!")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if(username == ""): return HttpResponse("No Username!")
        if(password == ""): return HttpResponse("No password!")
        if(email == ""): return HttpResponse("No email!")
        created = User.objects.create_user(username=username, password=password, email=email)
        user = authenticate(username=username, password=password)
        if (user is None):
            return HttpResponse("Unauthorized!")
        else:
            login(request, user)
            return redirect('portfolio//')
    return render(request, 'portfolio/register.html')
