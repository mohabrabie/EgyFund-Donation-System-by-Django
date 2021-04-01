from django.db import models
from django import forms
from django.utils import timezone

from accounts.models import CustomUser
from .category import Category
from .tag import Tag


def get_default_category():
    """ get a default value for Category; create new Category if not available """
    return Category.objects.get_or_create(name="donation-based")[0].id


class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField(max_length=100)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects', default=get_default_category)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    tags = models.ManyToManyField(Tag) 
    user = models.ForeignKey(CustomUser, on_delete=models.NOT_PROVIDED)

    def __str__(self):
        return self.title

    # # Logic for raising error if end_date < start_date
    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get("start_date")
    #     end_date = cleaned_data.get("end_date")
    #     if end_date < start_date:
    #         raise forms.ValidationError("End date should be greater than start date.")
