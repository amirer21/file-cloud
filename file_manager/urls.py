from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('download-selected/', views.download_selected, name='download_selected'),
]
