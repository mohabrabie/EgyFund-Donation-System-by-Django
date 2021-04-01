from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator
from django.utils import timezone


from .project import Project


class Donation(models.Model):
    donation = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.__str__() + self.user.__str__() + str(self.donation)
