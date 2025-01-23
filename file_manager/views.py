import os
import random
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.conf import settings
from zipfile import ZipFile
from io import BytesIO


# 파일 경로 설정
BASE_DIR = "/mnt/e/내보내기/2025-01-피아노"  # WSL에서의 실제 경로

def file_list(request):
    # 미리보기 파일 목록 가져오기
    preview_images = [
        f for f in os.listdir(BASE_DIR) if f.endswith('.jpg')
    ]

    return render(request, 'file_manager/file_list.html', {
        'images': preview_images,  # 미리보기 이미지 목록 전달
    })


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
