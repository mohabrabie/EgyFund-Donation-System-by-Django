from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, project

urlpatterns = [
    path('', home.index, name='egyfund'),
    path('project/add', project.create, name='project_add'),
    #* This is for testing only
    path('projects/', project.show_all, name='myprojects'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
