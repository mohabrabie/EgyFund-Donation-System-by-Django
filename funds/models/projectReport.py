from django.db import models
from accounts.models import CustomUser
from .project import Project


class ProjectReport(models.Model):
    report = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.__str__() + ", " + self.report
