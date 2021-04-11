from django import forms
from django.utils.translation import gettext_lazy as _

from .models.project import Project
from .models.projectPicture import ProjectPicture


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']
        fields = [
            'title',
            'details',
            'category',
            'tags',
            'total_target',
            'start_date',
            'end_date',
        ]
        labels = {
            'title': _('Project Title'),
            'details': _('Details'),
            'category': _('Category'),
            'tags': _('Tags'),
            'total_target': _('Total Target'),
            'start_date': _('Start Date'),
            'end_date': _('End Date'),
        }


class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectPicture
        fields = ['image', ]
