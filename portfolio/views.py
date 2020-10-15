from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
#from django.http import HttpResponse, HttpResponseNotFound, request, response
from django.views import generic, View
from django.core.exceptions import ViewDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger

from .models import Picture
# Create your views here.


class detail(generic.DetailView):
    model = Picture
    template_name = 'portfolio/picture.html'


class list(generic.ListView):
    template_name = 'portfolio/list.html'
    context_object_name = 'latest_picture_list'

    def get_queryset(self):
        """Return the last five published pictures."""
        return Picture.objects.all()


def display(request):
    all_picture = Picture.objects.all()
    paginator = Paginator(all_picture, 5)
    pages = request.GET.get('page', 1)
    #messages.warning(request, "This page will list all the picture", extra_tags='alert')
    try:
        all_picture = paginator.page(pages)
    except PageNotAnInteger:
        all_picture = paginator.page(1)
    return render(request, 'portfolio/display.html', {'all_picture': all_picture})


def index(request):
    return HttpResponse("Hello there, e-commerce store front coming here..")