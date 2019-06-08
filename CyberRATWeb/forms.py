from django import forms

class EmailForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100,
                           widget=forms.TextInput(attrs={'class': "form-control", "placeholder": "name"}))
    email = forms.CharField(label='Email ',
                            max_length=100, widget=forms.TextInput(attrs={'class': "form-control", "placeholder": "email"}))

