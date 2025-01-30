"""
Django settings for cloud_server project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(fxe(^^*cve6jzk!8t7#u8ci7t$8*+%ctij98urd*+@jwo#olh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '175.208.213.7', 'devmiro.co.kr', 'www.devmiro.co.kr']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'file_manager',
    'social_django',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.kakao.KakaoOAuth2',  # 카카오 OAuth 백엔드 추가
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cloud_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',  # MEDIA_URL 사용 가능
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cloud_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = '/mnt/e/내보내기/2025-01-피아노'
print(f"Media root: {MEDIA_ROOT}")
#MEDIA_ROOT = r"C:\Users\amire\python_workspace\HongCloud\cloud_server\media"
                
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    "/mnt/e/내보내기/2025-01-피아노",  # Windows 경로를 Raw 문자열로 추가
    "/home/hong/python-workspace/file-cloud",  # 실제 경로 추가
    "/home/hong/python-workspace/file-cloud/static/images",  # Favicon 파일이 있는 경로 추가
    ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIAL_AUTH_KAKAO_KEY = 'MY_KAKAO_APP_KEY'
SOCIAL_AUTH_KAKAO_REDIRECT_URI = 'http://www.devmiro.co.kr/accounts/complete/kakao/'
SOCIAL_AUTH_KAKAO_SCOPE = ['friends']


# Redirect URL 설정
LOGIN_URL = '/accounts/login/kakao/'  # 카카오 로그인 URL
LOGIN_REDIRECT_URL = '/download-list/'  # 로그인 성공 후 이동할 URL
LOGOUT_REDIRECT_URL = '/'  # 로그아웃 후 이동할 URL
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'  # 로그인 오류 시 이동할 URL

# HTTPS 강제 여부 (개발 환경에서는 False)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',       # 소셜 사용자 세부정보 가져오기
    'social_core.pipeline.social_auth.social_uid',           # 소셜 UID 가져오기
    'social_core.pipeline.social_auth.auth_allowed',         # 인증 허용 여부 확인
    'social_core.pipeline.social_auth.social_user',          # 소셜 사용자 확인
    'social_core.pipeline.user.get_username',               # 사용자 이름 생성
    'social_core.pipeline.user.create_user',                # 사용자 생성
    'social_core.pipeline.social_auth.associate_user',       # 소셜 계정과 사용자 연결
    'social_core.pipeline.social_auth.load_extra_data',      # 추가 데이터 로드
    'social_core.pipeline.user.user_details',               # 사용자 세부 정보 업데이트
)


# my_app/pipelines.py 파일을 생성하고 아래 내용을 추가
def activate_user(backend, user, response, *args, **kwargs):
    if user:
        user.is_active = True
        user.save()


GEOIP_PATH = '/usr/share/GeoIP/'