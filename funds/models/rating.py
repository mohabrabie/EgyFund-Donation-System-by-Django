from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
from .project import Project


class Rating(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    project = models.ForeignKey(Project, on_delete=models.NOT_PROVIDED)
    user = models.ForeignKey(CustomUser, on_delete=models.NOT_PROVIDED)

    def __str__(self):
        return self.project.__str__() + self.user.__str__() + str(self.rating)

