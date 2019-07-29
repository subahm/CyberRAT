from django import forms
from CyberRATWeb.models import Search


class SearchForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your name here"}))
    email = forms.CharField(widget=forms.TextInput(attrs={ "placeholder": "Enter your email here"}))
    facebook_link = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Enter link to your Facebook profile"}))
    instagram_link = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Enter link to your Instagram profile"}))
    twitter_link = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Enter link to your Twitter profile"}))


    class Meta:
        model = Search

        fields = ('name', 'email', 'facebook_link', 'instagram_link', 'twitter_link')
