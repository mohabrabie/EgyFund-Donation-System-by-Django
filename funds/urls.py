from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, project

urlpatterns = [
    path('', home.index, name='egyfund'),
    path('project/add', project.create, name='project_add'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)