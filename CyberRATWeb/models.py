from django.db import models
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class EmailForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.CharField(label='Email ', max_length=100)