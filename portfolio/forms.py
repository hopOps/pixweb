from django import forms


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

