import os
from os import listdir
from os.path import join, isfile, isdir

import random
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.conf import settings
from zipfile import ZipFile
from io import BytesIO
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import requests
import logging

logger = logging.getLogger(__name__)

# 파일 경로 설정
BASE_DIR = "/mnt/e/내보내기/2025-01-피아노"  # WSL에서의 실제 경로


def login_view(request):
    return render(request, 'login.html')  # 간단한 로그인 페이지
    

@login_required
def protected_download_list(request):
    kakao_token = request.user.social_auth.get(provider='kakao').extra_data.get('access_token', None)

    if not kakao_token:
        return render(request, 'file_manager/unauthorized.html', {
            'error_message': 'Kakao authentication failed. Please log in again.'
        }, status=403)

    # 이미지 루트 디렉터리 설정
    image_dir = '/home/hong/python-workspace/file-cloud/static/images/'
    categories = ["4waves", "hoon", "hari", "jaelin", "soyeon"]  # 탭에 해당하는 폴더 이름

    # 카테고리별 이미지 리스트 저장
    images_by_category = {}

    # 각 카테고리 폴더에서 이미지 수집
    for category in categories:
        category_path = join(image_dir, category)
        if isdir(category_path):  # 폴더가 존재하면
            images_by_category[category] = [
                f for f in listdir(category_path) 
                if isfile(join(category_path, f)) and f.endswith(('.jpg', '.png', '.gif'))
            ]
        else:
            images_by_category[category] = []  # 폴더가 없으면 빈 리스트

    # 분류되지 않은 루트 이미지를 추가
    # images_by_category["root"] = [
    #     f for f in listdir(image_dir) 
    #     if isfile(join(image_dir, f)) and f.endswith(('.jpg', '.png', '.gif'))
    # ]

    # 렌더링
    return render(request, 'file_manager/file_list.html', {
        'user': request.user,
        'images_by_category': images_by_category  # 카테고리별 이미지 전달
    })
    

# @login_required
# def download_list(request):
#     # 정적 파일 디렉터리에서 이미지 가져오기
#     image_dir = os.path.join(settings.STATIC_ROOT, 'images')
#     print(f"Image directory: {image_dir}")
#     images = [f for f in listdir(image_dir) if f.endswith(('.jpg', '.png', '.gif'))]
#     print(f"Images: {images}")
#     return render(request, 'file_manager/file_list.html', {
#         'images': images  # 이미지 파일 이름 리스트 반환
#     })


# def file_list(request):
#     # 정적 파일 디렉터리에서 이미지 가져오기
#     image_dir = os.path.join(settings.STATIC_ROOT, 'images')
#     print(f"Image directory: {image_dir}")
#     images = [f for f in listdir(image_dir) if f.endswith(('.jpg', '.png', '.gif'))]
#     print(f"Images: {images}")
#     return render(request, 'file_manager/file_list.html', {
#         'images': images  # 이미지 파일 이름 리스트 반환
#     })

def download_selected(request):
    if request.method == "POST":
        selected_images = request.POST.getlist('selected_images')
        #base_dir = "/mnt/e/사진 정리 64(2025.01 피아노)"
        base_dir = "/mnt/e/내보내기/2025-01-피아노"

        # Create a ZIP file in memory
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            for image in selected_images:
                nef_path = os.path.join(base_dir, image.replace('.jpg', '.NEF'))
                if os.path.exists(nef_path):
                    zip_file.write(nef_path, arcname=os.path.basename(nef_path))

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=selected_images.zip'
        return response

    return HttpResponse("Invalid request method", status=400)


def gallery(request):
    return render(request, 'file_manager/gallery.html')


def gallery_view(request):
    # 이미지 파일이 있는 실제 경로
    images_folder = '/home/hong/python-workspace/file-cloud/images'
    
    # 'DSC_'로 시작하고 '.jpg'로 끝나는 파일 필터링
    all_images = [f for f in os.listdir(images_folder) if f.startswith('DSC_') and f.endswith('.jpg')]
    
    # 이미지 URL을 생성할 수 있도록 절대 경로 전달
    context = {
        'images': all_images,
        'image_base_url': '/static/images/',  # 수정 후 여기에 실제 정적 파일 경로와 일치하게 설정
    }
    return render(request, 'file_manager/gallery.html', context)



