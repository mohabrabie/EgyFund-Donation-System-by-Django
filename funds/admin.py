from django.contrib import admin
from .models.project import Project
from .models.category import Category
from .models.tag import Tag
from .models.donation import Donation
from .models.comment import Comment
from .models.projectReport import ProjectReport
from .models.commentReport import CommentReport
from .models.rating import Rating
from .models.projectPicture import ProjectPicture


class ProjectPictureInLine(admin.StackedInline):
    model = ProjectPicture
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectPictureInLine,
    ]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Donation)
admin.site.register(Comment)
admin.site.register(ProjectReport)
admin.site.register(CommentReport)
admin.site.register(Rating)
admin.site.register(ProjectPicture)
