from django.db import models
from accounts.models import CustomUser
from .project import Project
from django.utils import timezone


class ProjectReport(models.Model):
    report = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def formatted_date(self):
        return self.created_at.strftime("%h %d, %Y at %H:%M")

    def __str__(self):
        return f"{self.user.username} reported {self.comment.project} project on {self.formatted_date()}"
