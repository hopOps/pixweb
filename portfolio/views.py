from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound, request, response
from django.views import generic, View
from django.core.exceptions import ViewDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from .models import Picture, Profile
from .forms import EditUser
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


# def isUser(user):
#     return user.username == "staff"


# @user_passes_test(isUser, login_url="/login")
def mygallery(request):
    user = User.objects.only('id').get(username=request.user)
    all_picture = Picture.objects.filter(user=user)
    paginator = Paginator(all_picture, 5)
    pages = request.GET.get('page', 1)
    try:
        all_picture = paginator.page(pages)
    except PageNotAnInteger:
        all_picture = paginator.page(1)
    return render(request, 'portfolio/mygallery.html', {'all_picture': all_picture})


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
            return redirect('portfolio')
    return render(request, 'portfolio/register.html')


@login_required
def edit_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EditUser(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = request.user
            profile, created = Profile.objects.get_or_create(user=request.user)
            # obj = Listing()  # gets new object
            user.profile.phone = form.cleaned_data['phone']
            user.profile.num_ftf = form.cleaned_data['num_ftf']
            user.profile.address = form.cleaned_data['address']
            user.profile.postal_code = form.cleaned_data['postal_code']
            user.profile.city = form.cleaned_data['city']
            user.profile.site_web = form.cleaned_data['site_web']
            user.profile.instagram = form.cleaned_data['instagram']
            user.profile.flickr = form.cleaned_data['flickr']
            user.profile.facebook = form.cleaned_data['facebook']
            user.profile.twitter = form.cleaned_data['twitter']
            # form.cleaned_data
            user.profile.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/portfolio')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditUser()

    return render(request, 'portfolio/edit_user.html', {'form': form})
