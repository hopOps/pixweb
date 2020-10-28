from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_http_methods
#from django.http import HttpResponse, HttpResponseNotFound, request, response
from django.views import generic, View
from django.core.exceptions import ViewDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

from .models import Picture, Profile
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
            return redirect('/portfolio')
    return render(request, 'portfolio/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, "Successfully logged out!")
    return render(request, 'portfolio/index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        num_ftf = request.POST['num_ftf']
        email = request.POST['email']
        if(username == ""): return HttpResponse("No Username!")
        if(password == ""): return HttpResponse("No password!")
        if(email == ""): return HttpResponse("No email!")
        if (num_ftf == ""): return HttpResponse("No numero ftf!")
        created = User.objects.create_user(username=username, password=password, email=email)
        user = authenticate(username=username, password=password)
        if (user is None):
            return HttpResponse("Unauthorized!")
        else:
            login(request, user)
            profile, created = Profile.objects.get_or_create(user=request.user)
            user.profile.num_ftf = num_ftf
            user.save()
            return redirect('/')
    return render(request, 'portfolio/register.html')


def edit_user(request):
    if request.method == 'POST':
        user = request.user
        phone = request.POST['phone']
        address = request.POST['address']
        postal_code = request.POST['postal_code']
        city = request.POST['city']
        site_web = request.POST['site_web']
        instagram = request.POST['instagram']
        flickr = request.POST['flickr']
        facebook = request.POST['facebook']
        twitter = request.POST['twitter']
        profile, created = Profile.objects.get_or_create(user=request.user)
        user.profile.phone = phone
        user.profile.address = address
        user.profile.postal_code = postal_code
        user.profile.city = city
        user.profile.site_web = site_web
        user.profile.instagram = instagram
        user.profile.flickr = flickr
        user.profile.facebook = facebook
        user.profile.twitter = twitter
        user.save()
    return render(request, 'portfolio/edit_user.html')
