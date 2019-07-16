
from django.urls import path
from . import views


urlpatterns = [
    path('projetos/', views.projects_list, name='projects'),
    path('pastas/<folder>', views.folders_list, name='folders'),
    path('topfolder/<projeto>', views.topfolders, name='topfolders'),
    path('upload/', views.upload, name='upload'),
]
