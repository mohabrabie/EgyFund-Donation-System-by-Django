from django.db import models
from accounts.models import CustomUser
from .comment import Comment


class CommentReport(models.Model):
    report = models.CharField(max_length=100)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment.__str__() + ", " + self.report
