import os
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.conf import settings
from zipfile import ZipFile
from io import BytesIO


def file_list(request):
    # 변환된 파일 목록 가져오기
    converted_images = [f for f in os.listdir(settings.MEDIA_ROOT) if f.endswith('.jpg')]

    # 동영상 파일 목록
    BASE_DIR = r"E:\사진 정리 64(2025.01 피아노)"
    videos = [f for f in os.listdir(BASE_DIR) if f.endswith(('.mp4', '.avi', '.mkv'))]

    return render(request, 'file_manager/file_list.html', {
        'images': converted_images,
        'videos': videos,
    })


def download_selected(request):
    if request.method == "POST":
        selected_images = request.POST.getlist('selected_images')
        base_dir = r"E:\사진 정리 64(2025.01 피아노)"

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

