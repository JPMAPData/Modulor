
from django.urls import path
from . import views


urlpatterns = [
    path('projetos/', views.projects_list, name='projects'),
    path('pastas/', views.folders_list, name='folders'),
    path('topfolder/', views.topfolders, name='topfolders'),
]
