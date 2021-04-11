from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from .customAccountManager import CustomAccountManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Mandatory fields
    email = models.EmailField(unique=True)
    username = models.CharField(_('User Name'), max_length=150)
    first_name = models.CharField(_('First Name'), max_length=150)
    last_name = models.CharField(_('last Name'), max_length=150)
    phone_number = models.CharField(max_length=11, null=False)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    # Optional fields
    birth_date = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True, null=True)
    country = CountryField(
        blank_label='(select country)', null=True, blank=True)

    # Meta fields (Used by django)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.email
