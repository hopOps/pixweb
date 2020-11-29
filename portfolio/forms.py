from django import forms
from .models import Category


# LIST CATEGORIES (iterable)
def get_available_categories():
    categories = ()
    for item in Category.objects.all():
        categories = categories + (((item.name), (item.name)),)
    return categories


class UpdatePicture(forms.Form):
    name = forms.CharField(label='Name', max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    category = forms.ChoiceField(choices=get_available_categories())
    description = forms.CharField(label='Description', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Description'}))
    photo = forms.ImageField()
    # public = forms.BooleanField()
