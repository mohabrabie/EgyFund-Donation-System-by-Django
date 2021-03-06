from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, project

urlpatterns = [
    path('', home.index, name='egyfund'),
    path('project/add', project.create, name='project_add'),
    url(r'^project/(?P<project_id>\d+)/$', project.read, name='project_read'),
    url(r'^project/(?P<project_id>\d+)/delete$', project.delete, name='project_delete'),
    url(r'^(?P<category_id>\d+)/$', home.listCategoryProjects, name='project_cat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
