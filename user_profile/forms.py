from django import forms


class EditUser(forms.Form):
    phone = forms.CharField(label='Phone Number', max_length=10, widget=forms.TextInput(attrs={'placeholder': 'phone'}))
    num_ftf = forms.CharField(label="FTF Number", max_length=4, widget=forms.TextInput(attrs={'placeholder': 'FTF Number'}))
    address = forms.CharField(label="Address", max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    postal_code = forms.CharField(label="Code Postal", max_length=5, required=False, widget=forms.TextInput(attrs={'placeholder': 'Code Postal'}))
    city = forms.CharField(label="City", max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    site_web = forms.URLField(label="WebSite", max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'WebSite'}))
    instagram = forms.URLField(label="instagram", max_length=40, required=False, widget=forms.TextInput(attrs={'placeholder': 'instagram'}))
    flickr = forms.URLField(label="flickr", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'flickr'}))
    facebook = forms.URLField(label="facebook", max_length=40, required=False, widget=forms.TextInput(attrs={'placeholder': 'facebook'}))
    twitter = forms.URLField(label="twitter", max_length=40, required=False, widget=forms.TextInput(attrs={'placeholder': 'twitter'}))


