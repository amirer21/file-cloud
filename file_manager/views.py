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
from django.core.paginator import Paginator
import requests
import logging
from .models import VisitorLog
from .models import UserActionLog
from user_agents import parse
from django.contrib.gis.geoip2 import GeoIP2
from django.utils.timezone import localtime
from django.contrib.auth import logout


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
def logout_view(request):
    """카카오 로그아웃 처리 후 Django 세션 삭제"""
    try:
        log_visitor(request)  # 방문 기록 저장

        kakao_token = request.user.social_auth.get(provider='kakao').extra_data.get('access_token', None)
        if kakao_token:
            kakao_logout_url = "https://kapi.kakao.com/v1/user/logout"
            headers = {
                "Authorization": f"Bearer {kakao_token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            response = requests.post(kakao_logout_url, headers=headers)

            if response.status_code != 200:
                logger.error(f"Kakao logout API failed: {response.text}")

        # Django 세션 로그아웃
        logout(request)

        # 세션 삭제 후 `cycle_key()`를 사용하여 새로운 세션을 유지
        request.session.flush()
        request.session.cycle_key()  # 새 세션 키 생성 (기존 OAuth state 값 유지)

        # 캐시 방지 및 강제 리디렉트
        response = redirect(settings.LOGOUT_REDIRECT_URL)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    except Exception as e:
        logger.error(f"Unexpected error in logout_view: {e}")
        return render(request, 'file_manager/unauthorized.html', {
            'error_message': 'An error occurred while logging out. Please try again.'
        }, status=500)




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
        selected_category = request.POST.get("selected_category", "unknown")  # 선택된 탭 가져오기
        base_dir = "/home/hong/python-workspace/file-cloud/staticfiles"

        if not selected_images:
            return HttpResponse("No files selected.", status=400)

        # 현재 시간 기반으로 파일명 생성
        timestamp = localtime(now()).strftime("%Y%m%d_%H%M%S")
        zip_filename = f"{selected_category}_{timestamp}.zip"

        # 로그 기록
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
        file_names = ", ".join(selected_images)

        UserActionLog.objects.create(
            ip_address=ip_address,
            action_type="Download",
            file_names=file_names,
            user_agent=user_agent,
        )

        # 파일 압축
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
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
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
        user_agent_str = request.META.get('HTTP_USER_AGENT', 'Unknown')

        # User-Agent 분석
        user_agent = parse(user_agent_str)
        browser = user_agent.browser.family if user_agent.browser.family else "Unknown"
        operating_system = user_agent.os.family if user_agent.os.family else "Unknown"

        # GeoIP를 사용하여 위치 정보 가져오기
        country, city = "Unknown", "Unknown"
        try:
            geo = GeoIP2()
            location = geo.city(ip_address)
            country = location.get("country_name", "Unknown")
            city = location.get("city", "Unknown")
        except Exception as e:
            logger.error(f"GeoIP lookup error: {e}")

        # 기타 요청 정보
        referer_url = request.META.get('HTTP_REFERER', '')
        request_url = request.path
        http_method = request.method
        session_id = request.session.session_key if request.session.session_key else ""

        # 로그인한 사용자 정보 (익명 사용자라면 None)
        user = request.user if request.user.is_authenticated else None

        # 방문 로그 저장
        VisitorLog.objects.create(
            ip_address=ip_address,
            user_agent=user_agent_str,
            browser=browser,
            operating_system=operating_system,
            country=country,
            city=city,
            referer_url=referer_url,
            request_url=request_url,
            http_method=http_method,
            session_id=session_id,
            user=user,
            visit_time=now()
        )

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
        visitor_logs_qs = VisitorLog.objects.order_by("-visit_time")
        user_logs_qs = UserActionLog.objects.order_by("-action_time")

        # 페이징 처리 (한 페이지에 50개씩)
        visitor_paginator = Paginator(visitor_logs_qs, 50)
        user_paginator = Paginator(user_logs_qs, 50)
        
        visitor_page_number = request.GET.get("visitor_page", 1)
        user_page_number = request.GET.get("user_page", 1)

        visitor_logs = visitor_paginator.get_page(visitor_page_number)
        user_logs = user_paginator.get_page(user_page_number)

        return render(request, "file_manager/visitor_logs.html", {
            "visitor_logs": visitor_logs,
            "user_logs": user_logs
        })

    except DatabaseError as e:
        logger.error(f"Database error in visitor_logs: {e}")
        return HttpResponse("An error occurred while retrieving logs.", status=500)
    except Exception as e:
        logger.error(f"Unexpected error in visitor_logs: {e}")
        return HttpResponse("An error occurred while processing your request.", status=500)