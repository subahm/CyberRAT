from django import forms
from CyberRATWeb.models import Search


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search

        fields = ('name', 'email', 'facebook_link')

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control", "placeholder": "name"}),
            'text': forms.TextInput(attrs={'class': "form-control", "placeholder": "email"}),
            'facebook_link': forms.TextInput(attrs={'class': "form-control", "placeholder": "facebook_link"})
        }