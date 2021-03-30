from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator


# Create your models here.
from .project import Project


class Donation(models.Model):
    donation = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    project = models.ForeignKey(Project, on_delete=models.NOT_PROVIDED)
    user = models.ForeignKey(CustomUser, on_delete=models.NOT_PROVIDED)

    def __str__(self):
        return self.project.__str__() + self.user.__str__() + str(self.donation)


