from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_view, name='gallery_view'),  # '/'는 gallery_view로 연결
    #path('download-list/', views.file_list, name='file_list'),  # '/downloadList/'는 file_list.html에 연결
    path('gallery/', views.gallery, name='gallery'),  # gallery.html에 연결    
    path('download-list/', login_required(views.protected_download_list), name='download_list'),
]
