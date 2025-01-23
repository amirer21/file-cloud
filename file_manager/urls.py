from django.urls import path
from . import views

urlpatterns = [
    # path('', views.file_list, name='file_list'),  # 기존 첫 페이지
    # path('download-selected/', views.download_selected, name='download_selected'),
    # path('gallery/', views.gallery, name='gallery'),  # 갤러리 페이지 추가
    path('', views.gallery_view, name='gallery_view'),  # '/'는 gallery_view로 연결
    path('download-list/', views.file_list, name='file_list'),  # '/downloadList/'는 file_list.html에 연결
    path('gallery/', views.gallery, name='gallery'),  # gallery.html에 연결
]
