from django.db import models
from accounts.models import CustomUser
from .project import Project


class Comment(models.Model):
    comment = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.NOT_PROVIDED)
    user = models.ForeignKey(CustomUser, on_delete=models.NOT_PROVIDED)

    def __str__(self):
        return self.project.__str__() + self.user.__str__() + self.comment
