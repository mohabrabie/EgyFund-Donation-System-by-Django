from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CreateUserForm(UserCreationForm):
    # error_css_class = 'error'
    # required_css_class = 'required'

    class Meta:
        model = CustomUser
        # Specify the fields from the model you want added
        fields = ["email", "first_name", "last_name", "username", "password1", "password2", "phone_number"]



