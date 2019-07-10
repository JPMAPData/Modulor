
from django.urls import path
from . import views


urlpatterns = [
    path('pastas/', views.folders_list, name='pastas'),
]
