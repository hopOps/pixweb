from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound, request, response, JsonResponse
from django.views import generic, View
from django.core.exceptions import ViewDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from json import dumps
from rest_framework import serializers

from .models import Picture, Profile, Category
from .forms import EditUser, UpdatePicture
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


@login_required(login_url="/portfolio/login")
def gallery(request):
    all_picture = Picture.objects.filter(public=False).order_by('pub_date')
    paginator = Paginator(all_picture, 5)
    pages = request.GET.get('page', 1)
    #messages.warning(request, "This page will list all the picture", extra_tags='alert')
    try:
        all_picture = paginator.page(pages)
    except PageNotAnInteger:
        all_picture = paginator.page(1)
    return render(request, 'portfolio/gallery.html', {'all_picture': all_picture})


def carousel(request, picture_id):
    picture = Picture.objects.get(pk=picture_id)
    all_picture = Picture.objects.filter(public=False)[:3]
    next_picture = Picture.objects.filter(id__gt=picture_id).order_by('pk').first()
    prev_picture = Picture.objects.filter(id__lt=picture_id).order_by('pk').last()
    current_list = [picture, next_picture, prev_picture]
    #paginator = Paginator(all_picture, 1)
    #pages = request.GET.get('page', 1)
    #try:
    #    all_picture = paginator.page(pages)
    #except PageNotAnInteger:
    #    all_picture = paginator.page(1)
    #context = {'all_picture': all_picture}
    context = {'picture': picture, 'all_picture': all_picture, 'next_picture': next_picture, 'prev_picture': prev_picture, 'current_list': current_list}
    return render(request, 'portfolio/carousel.html', context)



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


@login_required(login_url="/portfolio/login")
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
            return HttpResponseRedirect('portfolio/index.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditUser()

    return render(request, 'portfolio/edit_user.html', {'form': form})

#
# def handle_uploaded_image(i):
#     # resize image
#     imagefile  = StringIO.StringIO(i.read())
#     imageImage = Image.open(imagefile)
#
#     (width, height) = imageImage.size
#     (width, height) = scale_dimensions(width, height, longest_side=240)
#
#     resizedImage = imageImage.resize((width, height))
#
#     imagefile = StringIO.StringIO()
#     resizedImage.save(imagefile,'JPEG')
#     filename = hashlib.md5(imagefile.getvalue()).hexdigest()+'.jpg'
#
#     # #save to disk
#     imagefile = open(os.path.join('/tmp',filename), 'w')
#     resizedImage.save(imagefile,'JPEG')
#     imagefile = open(os.path.join('/tmp',filename), 'r')
#     content = django.core.files.File(imagefile)
#
#     my_object = MyDjangoObject()
#     my_object.photo.save(filename, content)



@login_required(login_url="/portfolio/login")
def upload_picture(request):

    if request.method == "POST":
        form = UpdatePicture(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(username=request.user)
            picture.user = user
            picture.name = form.cleaned_data['name']
            get_category = form.cleaned_data['category']
            picture.category = Category.objects.get(name=get_category)
            picture.description = form.cleaned_data['description']
            picture.photo = form.cleaned_data['photo']
            # picture.public = form.clean_data['public']
            obj = Picture.objects.create(
                user=picture.user,
                name=picture.name,
                category=picture.category,
                description=picture.description,
                photo=picture.photo,
                public=False
            )
            obj.save()
            return HttpResponseRedirect('/portfolio/gallery')
    else:
        form = UpdatePicture()
    return render(request, "portfolio/upload_picture.html", {'form': form})


def send_dictionary(request):
    # create data dictionary
    dataDictionary = {
        'hello': 'World',
        'geeks': 'forgeeks',
        'ABC': 123,
        456: 'abc',
        14000605: 1,
        'list': ['geeks', 4, 'geeks'],
        'dictionary': {'you': 'can', 'send': 'anything', 3: 1}
    }
    # dump data
    dataJSON = dumps(dataDictionary)
    return render(request, 'portfolio/send_dictionary.html', {'data': dataJSON})


# def get_photo(request, picture_id):
def get_photo(request):
    # create data dictionary
    # picture = Picture.objects.get(pk=picture_id)
    all_picture = Picture.objects.filter(public=False)[:10]
    data = serializers.Serializer('json', all_picture)

    # dataJSON = MedicSerializer(all_picture, many=True)
    return render(request, 'portfolio/carouselv2.html', {'data': data})


def all_picture(request):
    all_picture = list(Picture.objects.values())
    return JsonResponse(all_picture, safe=False)