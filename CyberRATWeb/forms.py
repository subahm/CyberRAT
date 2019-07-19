from django import forms
from CyberRATWeb.models import Search


class SearchForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "input--style-1", "placeholder": "name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': "input--style-1", "placeholder": "email"}))
    facebook_link = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': "input--style-1", "placeholder": "facebook link"}))
    instagram_link = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': "input--style-1", "placeholder": "ex. https://www.instagram.com/USERNAME/"}))


    class Meta:
        model = Search

        fields = ('name', 'email', 'facebook_link', 'instagram_link')
