"""
URL configuration for cloud_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('file_manager.urls')),
    path('accounts/', include('social_django.urls', namespace='social')),  # 소셜 로그인 경로
    path('download-list/', include('file_manager.urls')),  # 다운로드 페이지
]

if settings.DEBUG:  # 개발 환경에서만 적용
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #r"E:\내보내기\2025-01-피아노",  # Windows 경로를 Raw 문자열로 추가
    #urlpatterns += static(settings.MEDIA_URL, document_root="/mnt/e/내보내기/2025-01-피아노")
