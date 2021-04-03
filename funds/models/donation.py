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
    
    def formatted_date(self):
        return self.date.strftime("%h %d, %Y")

    def __str__(self):
        return f"${str(self.donation)} donated for {self.project} project by {self.user.username} on {self.formatted_date()}"
