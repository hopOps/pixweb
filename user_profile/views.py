from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .forms import EditUser

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if(username == ""):
            messages.info(request, "No Username!")
            return redirect('/user_profile/login')
        if (password == ""):
            messages.info(request, "No password!")
            return redirect('/user_profile/login')
        user = authenticate(username=username, password=password)
        if(user is None):
            messages.info(request, "User is unauthorized !!!")
            return redirect('/user_profile/login')
        else:
            login(request, user)
            return redirect('/portfolio/')
    return render(request, 'user_profile/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, "Successfully logged out!")
    return render(request, 'portfolio/index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        num_ftf = request.POST['num_ftf']
        email = request.POST['email']
        if(username == ""): return HttpResponse("No Username!")
        if(password == ""): return HttpResponse("No password!")
        if(email == ""): return HttpResponse("No email!")
        if (num_ftf == ""): return HttpResponse("No numero ftf!")
        created = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname, email=email)
        user = authenticate(username=username, password=password)
        if (user is None):
            return HttpResponse("Unauthorized!")
        else:
            login(request, user)
            profile, created = Profile.objects.get_or_create(user=request.user)
            user.profile.num_ftf = num_ftf
            user.save()
            return redirect('/portfolio')
    return render(request, 'user_profile/register.html')


@login_required(login_url="/user_profile/login")
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
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditUser()

    return render(request, 'user_profile/edit_user.html', {'form': form})
