from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound, request, response, JsonResponse
from django.views import generic, View
from django.core.exceptions import ViewDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from json import dumps
from rest_framework import serializers

from user_profile.models import Profile
from django.contrib.auth.models import User
from .models import Picture, Category
from .forms import UpdatePicture

# Rest
from rest_framework import viewsets
from .serializers import PictureSerializer, CategorySerializer
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
    all_picture = Picture.objects.filter(user=user).order_by('pub_date')
    paginator = Paginator(all_picture, 5)
    pages = request.GET.get('page', 1)
    try:
        all_picture = paginator.page(pages)
    except PageNotAnInteger:
        all_picture = paginator.page(1)
    return render(request, 'portfolio/mygallery.html', {'all_picture': all_picture})


@login_required(login_url="/user_profile/login")
def gallery(request):
    all_picture = Picture.objects.filter(public=False).order_by('pub_date')
    all_category = Category.objects.all()
    paginator = Paginator(all_picture, 5)
    pages = request.GET.get('page', 1)
    #messages.warning(request, "This page will list all the picture", extra_tags='alert')
    try:
        all_picture = paginator.page(pages)
    except PageNotAnInteger:
        all_picture = paginator.page(1)
    return render(request, 'portfolio/gallery.html', {'all_picture': all_picture, 'all_category': all_category})


@login_required(login_url="/user_profile/login")
def galleryv2(request):
    all_picture = Picture.objects.filter(public=False).order_by('pub_date')
    pix_list = [all_picture[:5], all_picture[5:]]
    all_category = Category.objects.all()
    return render(request, 'portfolio/galleryv2.html', {'all_picture': pix_list, 'all_category': all_category})


def carousel(request, picture_id):
    picture = Picture.objects.get(pk=picture_id)
    all_picture = Picture.objects.filter(public=False)[:3]
    next_picture = Picture.objects.filter(id__gt=picture_id).order_by('pk').first()
    prev_picture = Picture.objects.filter(id__lt=picture_id).order_by('pk').last()
    current_list = [picture, next_picture, prev_picture]
    context = {'picture': picture, 'all_picture': all_picture, 'next_picture': next_picture, 'prev_picture': prev_picture, 'current_list': current_list}
    return render(request, 'portfolio/carousel.html', context)


def carouselv2(request, picture_id):
    picture = Picture.objects.get(pk=picture_id)
    next_picture = Picture.objects.filter(id__gt=picture_id).order_by('pk').first()
    prev_picture = Picture.objects.filter(id__lt=picture_id).order_by('pk').last()
    current_list = [picture, next_picture, prev_picture]
    context = {'picture': picture, 'next_picture': next_picture, 'prev_picture': prev_picture, 'current_list': current_list}
    return render(request, 'portfolio/carouselv2.html', context)


def index(request):
    return render(request, "portfolio/index.html")


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
            # Create and Save Picture
            obj = Picture.objects.create(
                user=picture.user,
                name=picture.name,
                category=picture.category,
                description=picture.description,
                photo=picture.photo,
                public=False
            )
            obj.save()
            # Change number to Add User photo Number !
            user_profile = Profile.objects.get(user=user.id)
            user_profile.nb_photo = user_profile.nb_photo + 1
            user_profile.save()
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


# def all_picture(request):
#     all_picture = list(Picture.objects.values())
#     return JsonResponse(all_picture, safe=False)


class pictures(viewsets.ModelViewSet):
    serializer_class = PictureSerializer
    queryset = Picture.objects.all()
