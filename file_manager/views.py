import os
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.conf import settings

# 동영상 및 변환된 이미지 목록 표시
def file_list(request):
    # 변환된 파일 목록 가져오기
    print(f"file_list Media root: {settings.MEDIA_ROOT}")
    converted_images = [f for f in os.listdir(settings.MEDIA_ROOT) if f.endswith('.jpg')]

    # 동영상 파일 목록
    BASE_DIR = r"E:\사진 정리 64(2025.01 피아노)"
    videos = [f for f in os.listdir(BASE_DIR) if f.endswith(('.mp4', '.avi', '.mkv'))]

    # 렌더링
    return render(request, 'file_manager/file_list.html', {
        'images': converted_images,
        'videos': videos,
    })

# 파일 다운로드
def download_file(request, file_name):
    BASE_DIR = r"E:\사진 정리 64(2025.01 피아노)"
    file_path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
        return response
    return HttpResponse("File not found", status=404)
