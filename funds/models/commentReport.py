from django.db import models
from accounts.models import CustomUser
from .comment import Comment
from django.utils import timezone


class CommentReport(models.Model):
    report = models.CharField(max_length=100)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def formatted_date(self):
        return self.created_at.strftime("%h %d, %Y at %H:%M")

    def __str__(self):
        return f"{self.user.username} reported {self.comment.user.username} in {self.comment.project} project on {self.formatted_date()}"
