from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from .project import Project


class Rating(models.Model):
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.__str__() + self.user.__str__() + str(self.rating)
