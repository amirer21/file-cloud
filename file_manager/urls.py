from django.contrib.auth import logout  # Django 로그아웃 함수 추가
from django.shortcuts import redirect
from django.urls import path
from . import views

# 로그아웃 뷰
def logout_view(request):
    logout(request)  # Django의 logout() 사용
    return redirect('/')  # 로그아웃 후 메인 페이지로 이동

urlpatterns = [
    path('', views.gallery_view, name='gallery_view'),
    path('gallery/', views.gallery, name='gallery'),
    path('download-list/', views.protected_download_list, name='download_list'),
    path('download-selected/', views.download_selected, name='download_selected'),
    path('visitor-logs/', views.visitor_logs, name='visitor_logs'),
    path('logout/', views.logout_view, name='logout'),  # 로그아웃 URL 추가

]
