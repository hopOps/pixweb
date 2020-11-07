from django import forms
from .models import Category


# LIST CATEGORIES (iterable)
def get_available_categories():
    categories = ()
    for item in Category.objects.all():
        categories = categories + (((item.name), (item.name)),)
    return categories


class EditUser(forms.Form):
    phone = forms.CharField(label='Phone Number', max_length=10, widget=forms.TextInput(attrs={'placeholder': 'phone'}))
    num_ftf = forms.CharField(label="FTF Number", max_length=4)
    address = forms.CharField(label="Address", max_length=100, required=False)
    postal_code = forms.CharField(label="Code Postal", max_length=5, required=False)
    city = forms.CharField(label="City", max_length=20, required=False)
    site_web = forms.URLField(label="WebSite", max_length=100, required=False)
    instagram = forms.URLField(label="instagram", max_length=40, required=False)
    flickr = forms.URLField(label="flickr", max_length=50, required=False)
    facebook = forms.URLField(label="facebook", max_length=40, required=False)
    twitter = forms.URLField(label="twitter", max_length=40, required=False)


class UpdatePicture(forms.Form):
    name = forms.CharField(label='Name', max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    category = forms.ChoiceField(choices=get_available_categories())
    description = forms.CharField(label='Description', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Description'}))
    photo = forms.ImageField()
    # public = forms.BooleanField()
