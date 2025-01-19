from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),  # 기존 첫 페이지
    path('download-selected/', views.download_selected, name='download_selected'),
    path('gallery/', views.gallery, name='gallery'),  # 갤러리 페이지 추가
]
