import os
from os import listdir
from os.path import join, isfile, isdir

import random
from django.http import HttpRequest
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.conf import settings
from zipfile import ZipFile
from io import BytesIO
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
import requests
import logging
from .models import VisitorLog
from .models import UserActionLog

logger = logging.getLogger(__name__)

# 파일 경로 설정
BASE_DIR = "/mnt/e/내보내기/2025-01-피아노"  # WSL에서의 실제 경로


def login_view(request):
    try:
        return render(request, 'login.html')
    except Exception as e:
        logger.error(f"Unexpected error in login_view: {e}")
        return HttpResponse("An error occurred while rendering the login page.", status=500)


@login_required
def protected_download_list(request):
    try:
        log_visitor(request)
        
        kakao_token = request.user.social_auth.get(provider='kakao').extra_data.get('access_token', None)
        if not kakao_token:
            return render(request, 'file_manager/unauthorized.html', {
                'error_message': 'Kakao authentication failed. Please log in again.'
            }, status=403)

        image_dir = '/home/hong/python-workspace/file-cloud/static/images/'
        categories = ["4waves", "hoon", "hari", "jaelin", "soyeon"]
        images_by_category = {}

        for category in categories:
            category_path = join(image_dir, category)
            if isdir(category_path):
                try:
                    images_by_category[category] = [
                        f for f in listdir(category_path) 
                        if isfile(join(category_path, f)) and f.endswith(('.jpg', '.png', '.gif'))
                    ]
                except OSError as e:
                    logger.error(f"Error accessing category {category}: {e}")
                    images_by_category[category] = []
            else:
                images_by_category[category] = []

        return render(request, 'file_manager/file_list.html', {
            'user': request.user,
            'images_by_category': images_by_category
        })
    except Exception as e:
        logger.error(f"Unexpected error in protected_download_list: {e}")
        return HttpResponse("An error occurred while processing your request.", status=500)

    

def download_selected(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=400)

    try:
        selected_images = request.POST.getlist("selected_images")
        base_dir = "/home/hong/python-workspace/file-cloud/staticfiles"

        if not selected_images:
            return HttpResponse("No files selected.", status=400)

        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
        file_names = ", ".join(selected_images)

        UserActionLog.objects.create(
            ip_address=ip_address,
            action_type="Download",
            file_names=file_names,
            user_agent=user_agent,
        )

        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for image_path in selected_images:
                full_path = os.path.join(base_dir, image_path)
                if os.path.exists(full_path):
                    zip_file.write(full_path, arcname=os.path.basename(full_path))
                else:
                    logger.warning(f"File not found: {full_path}")

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=selected_images.zip"
        return response
    except DatabaseError as e:
        logger.error(f"Database error in download_selected: {e}")
        return HttpResponse("An error occurred while logging user action.", status=500)
    except Exception as e:
        logger.error(f"Unexpected error in download_selected: {e}")
        return HttpResponse("An error occurred while processing your request.", status=500)




def gallery(request):
    try:
        log_visitor(request)
        return render(request, 'file_manager/gallery.html')
    except Exception as e:
        logger.error(f"Unexpected error in gallery: {e}")
        return HttpResponse("An error occurred while rendering the gallery.", status=500)



def gallery_view(request):
    try:
        log_visitor(request)
        images_folder = '/home/hong/python-workspace/file-cloud/images'

        try:
            all_images = [f for f in os.listdir(images_folder) if f.startswith('DSC_') and f.endswith('.jpg')]
        except FileNotFoundError:
            logger.error(f"Image directory not found: {images_folder}")
            all_images = []
        except OSError as e:
            logger.error(f"OS error accessing image directory: {e}")
            all_images = []

        context = {
            'images': all_images,
            'image_base_url': '/static/images/',
        }
        return render(request, 'file_manager/gallery.html', context)
    except Exception as e:
        logger.error(f"Unexpected error in gallery_view: {e}")
        return HttpResponse("An error occurred while processing the gallery view.", status=500)

def log_visitor(request: HttpRequest):
    """ 방문자 정보를 기록하는 함수 """
    try:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

        VisitorLog.objects.create(ip_address=ip_address, user_agent=user_agent, visit_time=now())
    except IntegrityError as e:
        logger.error(f"Database integrity error in log_visitor: {e}")
    except DatabaseError as e:
        logger.error(f"Database error in log_visitor: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in log_visitor: {e}")

def get_client_ip(request):
    """클라이언트의 실제 IP 주소를 가져오는 함수"""
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception as e:
        logger.error(f"Error getting client IP: {e}")
        return "Unknown"

def visitor_logs(request):
    try:
        visitor_logs = VisitorLog.objects.order_by("-visit_time")[:50]
        user_logs = UserActionLog.objects.order_by("-action_time")[:50]
        return render(request, "file_manager/visitor_logs.html", {"visitor_logs": visitor_logs, "user_logs": user_logs})
    except DatabaseError as e:
        logger.error(f"Database error in visitor_logs: {e}")
        return HttpResponse("An error occurred while retrieving logs.", status=500)
    except Exception as e:
        logger.error(f"Unexpected error in visitor_logs: {e}")
        return HttpResponse("An error occurred while processing your request.", status=500)