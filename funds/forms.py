from django import forms
from django.utils.translation import gettext_lazy as _
#* First run: pip install django-multiupload
# from multiupload.fields import MultiImageField

from .models.project import Project
from .models.projectPicture import ProjectPicture
from .models.tag import Tag


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

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectPicture
        fields = ['image', ]


#! This class depends on MutiImageField which most probably overrides the widget render method & I am still investigating,
#! would appreciate any help
# class ProjectForm(forms.ModelForm):
#     images = MultiImageField(min_num=1, max_num=20)

#     class Meta:
#         model = Project
#         exclude = ['user']
#         fields = [
#             'title',
#             'details',
#             'categories',
#             'tags',
#             'start_date',
#             'end_date',
#             'images',
#         ]
#         labels = {
#             'title': _('Project Title'),
#             'details': _('Details'),
#             'categories': _('Category'),
#             'tags': _('Tags'),
#             'start_date': _('Start Date'),
#             'end_date': _('End Date'),
#         }


#     def save(self, commit=True):
#         project_images = self.cleaned_data.pop('images')
#         project_instance = super(ProjectForm, self).save(commit)
#         for each_image in project_images:
#            project_picture_object = ProjectPicture(image=each_image,
#                                                    project=project_instance)
#            project_picture_object.save()

#         return project_instance

#     def render(self, name, value, attrs=None, renderer=None):
#         """Render the widget as an HTML string."""
#         context = self.get_context(name, value, attrs)
#         return self._render(self.template_name, context, renderer)
