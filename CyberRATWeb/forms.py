from django import forms
from CyberRATWeb.models import Search


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search

        fields = ('name', 'email', 'facebook_link', 'linkedin_link')

        widgets = {
            'name': forms.TextInput(attrs={'class': "input--style-1", "placeholder": "name"}),
            'email': forms.TextInput(attrs={'class': "input--style-1", "placeholder": "email"}),
            'facebook_link': forms.TextInput(attrs={'class': "input--style-1", "placeholder": "facebook link"}),
            'linkedin_link': forms.TextInput(attrs={'class': "input--style-1", "placeholder": "linkedin link"})
        }