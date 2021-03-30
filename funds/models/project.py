from django.db import models
from accounts.models import CustomUser


# Create your models here.
from .category import Category
from .tag import Tag


class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Project can have ONE category
    categories = models.ManyToManyField(Category)  # Project can have MANY category
    tags = models.ManyToManyField(Tag)   # Project can have MANY tags
    user = models.ForeignKey(CustomUser, on_delete=models.NOT_PROVIDED)

    def __str__(self):
        return self.title

