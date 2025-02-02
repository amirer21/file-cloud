# Dev Hong Cloud

## 📌 프로젝트 개요
**Dev Hong Cloud**는 이미지 파일을 관리하고, 다운로드하며, 갤러리로 구성된 웹 애플리케이션입니다. 
사용자는 카테고리별로 이미지를 확인하고, 선택한 이미지를 ZIP 파일로 다운로드할 수 있습니다. 
또한, 방문자 및 사용자 로그를 기록하고 관리하는 기능이 포함되어 있습니다.

---

## 🚀 주요 기능
1. **이미지 갤러리**
   - 카테고리별로 이미지를 표시합니다.
   - 간단한 UI/UX를 제공하여 사용자가 이미지를 탐색할 수 있습니다.

2. **파일 다운로드**
   - 선택한 이미지를 압축(ZIP) 파일로 다운로드할 수 있습니다.
   - 선택/해제 버튼으로 사용자가 쉽게 이미지를 선택할 수 있습니다.

3. **방문자 및 사용자 액션 로그**
   - 방문자의 IP, 디바이스 정보, 접속 시간을 기록합니다.
   - 다운로드 시 사용자 액션 로그(다운로드한 파일 목록 포함)를 기록합니다.

4. **카카오톡 로그인**
   - OAuth를 이용한 카카오톡 로그인 기능 제공.
   - 로그인된 사용자만 다운로드 기능을 이용할 수 있습니다.

---

## 🛠️ 기술 스택
- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (개발 환경) / PostgreSQL (배포 환경)
- **Authentication**: `social-auth-app-django` (카카오 OAuth 2.0)
- **Deployment**: Nginx + Docker

---

## 📂 프로젝트 구조
```
file-cloud/
├── file_manager/
│   ├── migrations/        # 데이터베이스 마이그레이션 파일
│   ├── static/            # 정적 파일 (이미지, CSS, JS)
│   ├── templates/         # HTML 템플릿
│   ├── models.py          # 데이터베이스 모델
│   ├── views.py           # 뷰 함수
│   ├── urls.py            # URL 라우팅
│   ├── admin.py           # 관리자 페이지 설정
│   ├── tests.py           # 단위 테스트
├── manage.py              # Django 관리 명령어
├── db.sqlite3             # SQLite 데이터베이스 파일
├── requirements.txt       # 의존성 패키지 리스트
```


---

## 🔧 설치 및 실행

### 1. **환경 설정**
Python 3.10 이상이 설치되어 있어야 합니다.

```bash
# 1. 프로젝트 클론
git clone https://github.com/amirer21/file-cloud.git
cd file-cloud

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 데이터베이스 마이그레이션
python manage.py migrate

# 5. 개발 서버 실행
python manage.py runserver
```

---

## 📂 정적 파일 관리 (Static Files)
Django에서는 정적 파일(이미지, CSS, JavaScript 등)을 `static/` 디렉터리에서 관리합니다. 이를 위해 정적 파일을 수집하고 서빙하는 과정이 필요합니다.

### 1. **정적 파일 설정** (settings.py)
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'file_manager/static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 2. **정적 파일 수집 명령어**
```bash
python manage.py collectstatic
```
- `collectstatic` 명령어는 프로젝트의 모든 정적 파일을 `STATIC_ROOT` 폴더로 모읍니다.
- 배포 환경에서는 `STATICFILES_DIRS`에 정의된 정적 파일을 한 곳에서 제공할 수 있도록 합니다.

---

## 📋 데이터베이스 모델

### 1. **VisitorLog (방문자 로그)**

방문자의 접속 정보를 기록하는 모델입니다.

| 필드          | 설명                             |
|---------------|--------------------------------|
| `ip_address`  | 방문자의 IP 주소               |
| `browser`     | 사용자의 브라우저 (예: Chrome) |
| `operating_system` | 운영체제 정보 (예: Windows, Mac) |
| `country`     | 접속 국가                      |
| `city`        | 접속 도시                      |
| `referer_url` | 사용자가 방문한 경로            |
| `request_url` | 방문한 URL                     |
| `http_method` | 요청 방식 (GET, POST 등)       |
| `session_id`  | Django 세션 ID                 |
| `visit_time`  | 방문 시간                      |

```python
class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소")
    browser = models.CharField(max_length=100, verbose_name="브라우저", blank=True)
    operating_system = models.CharField(max_length=100, verbose_name="운영체제", blank=True)
    country = models.CharField(max_length=50, verbose_name="접속 국가", blank=True)
    city = models.CharField(max_length=100, verbose_name="접속 도시", blank=True)
    referer_url = models.URLField(verbose_name="리퍼러 URL", blank=True, null=True)
    request_url = models.TextField(verbose_name="요청한 URL", default="/")
    http_method = models.CharField(max_length=10, verbose_name="요청 메서드", default="GET")
    session_id = models.CharField(max_length=100, blank=True, verbose_name="세션 ID")
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name="방문 시간")
```

---

### 2. **GeoIP2를 이용한 국가 및 도시 정보 추가**
Django의 `GeoIP2`를 사용하여 방문자의 국가 및 도시 정보를 자동으로 가져옵니다.

#### 📌 **설치 및 설정**
1. **필요한 패키지 설치**
   ```sh
   pip install maxminddb-geolite2
   ```
2. **GeoIP 데이터베이스 다운로드**
   ```sh
   mkdir -p /usr/share/GeoIP
   cd /usr/share/GeoIP
   wget https://raw.githubusercontent.com/P3TERX/GeoLite.mmdb/download/GeoLite2-City.mmdb
   ```
3. **Django 설정 (`settings.py`)**
   ```python
   GEOIP_PATH = "/usr/share/GeoIP"
   ```

---

### 3. **방문자 로그 저장 함수 (업데이트됨)**
`views.py`에서 방문자의 국가 및 도시 정보를 자동으로 저장하도록 수정되었습니다.

```python
from django.contrib.gis.geoip2 import GeoIP2

def log_visitor(request):
    """ 방문자 정보를 기록하는 함수 """
    try:
        ip_address = get_client_ip(request)
        user_agent_str = request.META.get('HTTP_USER_AGENT', 'Unknown')

        # User-Agent 분석
        user_agent = parse(user_agent_str)
        browser = user_agent.browser.family if user_agent.browser.family else "Unknown"
        operating_system = user_agent.os.family if user_agent.os.family else "Unknown"

        # GeoIP를 사용하여 위치 정보 가져오기
        country, city = get_location(ip_address)

        # 기타 요청 정보
        referer_url = request.META.get('HTTP_REFERER', '')
        request_url = request.path
        http_method = request.method
        session_id = request.session.session_key if request.session.session_key else ""

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
            visit_time=now()
        )

    except Exception as e:
        logger.error(f"Unexpected error in log_visitor: {e}")
```

---

### 4. **실제 IP 주소 확인 및 프록시 지원**
기존 `get_client_ip` 함수는 프록시 서버를 고려하지 않았으므로, **실제 클라이언트 IP를 가져오도록 개선**되었습니다.

```python
import ipaddress

def get_client_ip(request):
    """ 클라이언트의 실제 IP 주소를 가져오는 함수 (프록시 고려) """
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
            for ip in ip_list:
                if is_valid_ip(ip):
                    return ip  # 첫 번째 유효한 IP 반환
        
        x_real_ip = request.META.get('HTTP_X_REAL_IP')
        if x_real_ip and is_valid_ip(x_real_ip):
            return x_real_ip

        remote_addr = request.META.get('REMOTE_ADDR')
        if remote_addr and is_valid_ip(remote_addr):
            return remote_addr
        
        return "Unknown"
    except Exception as e:
        logger.error(f"Error getting client IP: {e}")
        return "Unknown"

def is_valid_ip(ip):
    """IP 주소가 유효한지 확인하는 함수"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
```

---

### 🚀 ** 방문자 로그 저장 방식**
이제 방문자 로그에는 **브라우저, 운영체제, 국가, 도시, HTTP 요청 메서드, 세션 ID** 등의 정보가 포함됩니다.

| IP 주소       | 브라우저 | 운영체제 | 국가     | 도시    | 요청 URL        | HTTP 메서드 | 방문 시간               |
|--------------|---------|---------|---------|--------|--------------|------------|----------------------|
| 172.26.208.1 | Chrome  | Windows | Unknown | Unknown | /download-list/ | GET        | Jan. 31, 2025, 1:07 a.m. |
| 8.8.8.8      | Firefox | Linux   | USA     | New York | /gallery/      | POST       | Jan. 31, 2025, 1:10 a.m. |

이제 국가 및 도시 정보도 함께 저장되며, 프록시 서버를 사용하는 경우에도 실제 클라이언트 IP를 올바르게 가져올 수 있습니다. 🚀

### 2. **UserActionLog**
사용자의 행동을 기록하는 모델.
| 필드            | 설명                       |
|-----------------|--------------------------|
| `ip_address`    | 사용자 IP 주소             |
| `action_type`   | 액션 타입 (예: Download)    |
| `file_names`    | 다운로드한 파일 목록        |
| `user_agent`    | 디바이스 정보              |
| `action_time`   | 액션 발생 시간             |

### 3. **모델 생성 및 마이그레이션 명령어**
```bash
# 모델 생성 후 마이그레이션 파일 생성
python manage.py makemigrations

# 데이터베이스에 적용
python manage.py migrate
```
- `makemigrations`: 모델 변경 사항을 감지하여 마이그레이션 파일을 생성합니다.
- `migrate`: 생성된 마이그레이션 파일을 적용하여 데이터베이스를 변경합니다.

---

(2025.02.02 updated)

## 📋 데이터베이스 모델

### 1. **VisitorLog (방문자 로그)**

방문자의 접속 정보를 기록하는 모델입니다.

| 필드          | 설명                             |
|---------------|--------------------------------|
| `ip_address`  | 방문자의 IP 주소               |
| `browser`     | 사용자의 브라우저 (예: Chrome) |
| `operating_system` | 운영체제 정보 (예: Windows, Mac) |
| `country`     | 접속 국가                      |
| `city`        | 접속 도시                      |
| `referer_url` | 사용자가 방문한 경로            |
| `request_url` | 방문한 URL                     |
| `http_method` | 요청 방식 (GET, POST 등)       |
| `session_id`  | Django 세션 ID                 |
| `visit_time`  | 방문 시간                      |

```python
class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소")
    browser = models.CharField(max_length=100, verbose_name="브라우저", blank=True)
    operating_system = models.CharField(max_length=100, verbose_name="운영체제", blank=True)
    country = models.CharField(max_length=50, verbose_name="접속 국가", blank=True)
    city = models.CharField(max_length=100, verbose_name="접속 도시", blank=True)
    referer_url = models.URLField(verbose_name="리퍼러 URL", blank=True, null=True)
    request_url = models.TextField(verbose_name="요청한 URL", default="/")
    http_method = models.CharField(max_length=10, verbose_name="요청 메서드", default="GET")
    session_id = models.CharField(max_length=100, blank=True, verbose_name="세션 ID")
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name="방문 시간")
```

---

### 2. **카카오 로그인 & 로그아웃 기능**
✅ **로그아웃 버튼 추가 (`gallery.html`)**
```html
<div class="button-container">
    {% if user.is_authenticated %}
        <a href="{% url 'download_list' %}" class="download-button">Download List</a>
        <a href="{% url 'logout' %}" class="logout-button">Logout</a>
    {% else %}
        <a href="{% url 'social:begin' 'kakao' %}" class="download-button">Login with Kakao</a>
    {% endif %}
</div>
```

✅ **로그아웃 API 구현 (`file_manager/views.py`)**
```python
import requests
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    """카카오 로그아웃 처리 후 Django 세션 삭제"""
    try:
        kakao_token = request.user.social_auth.get(provider='kakao').extra_data.get('access_token', None)
        if kakao_token:
            kakao_logout_url = "https://kapi.kakao.com/v1/user/logout"
            headers = {
                "Authorization": f"Bearer {kakao_token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            requests.post(kakao_logout_url, headers=headers)

        logout(request)
        return redirect('/')

    except Exception as e:
        print(f"Kakao logout error: {e}")
        return redirect('/')
```

✅ **Django URL 설정 (`file_manager/urls.py`)**
```python
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
]
```

---

## ✅ 향후 개선 예정 (Backlog)
✅ **Version 1.0.4** (UI 개선 및 사용자 기능 추가)  
🔹 **파일 정렬 및 필터 기능 추가**  
🔹 **검색 기능 추가**  
🔹 **카카오톡 친구 목록 API 활용하여 특정 사용자만 다운로드 가능하도록 제한**  
🔹 **RESTful API 지원 (파일 업로드 및 다운로드 API 제공)**  
🔹 **방문자 로그 검색 및 필터 기능 추가**  
🔹 **관리자 페이지에서 방문자 기록 대시보드 제공**  

---

## 🏗️ Nginx 설정 및 배포 명령어
Django 프로젝트를 Nginx를 사용하여 배포할 때 주요 설정과 실행 명령어는 다음과 같습니다.

### 1. **Nginx 설정 파일 예시**
```nginx
server {
    listen 80;
    server_name example.com;

    location /static/ {
        root /home/user/file-cloud/staticfiles;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. **Nginx 설정 적용 명령어**
```bash
# 설정 문법 검사
sudo nginx -t

# Nginx 서비스 재시작
sudo systemctl restart nginx

# Nginx 서비스 상태 확인
sudo systemctl status nginx
```

이러한 설정을 통해 Django 프로젝트를 안정적으로 배포하고 운영할 수 있습니다.

---

## 추가 이슈 사항

### ✅ WSL에서 `/mnt` 관련 문제 해결 및 설정 방법  

WSL(Windows Subsystem for Linux)에서는 Windows의 드라이브가 `/mnt/` 아래에 자동으로 마운트됩니다. 하지만 특정 상황에서 마운트가 실패하거나, 접근 권한 문제가 발생할 수 있습니다.

---

## 📌 **1. `/mnt/e/` 드라이브가 마운트되지 않는 경우**
`ls` 명령어로 `/mnt/` 아래의 마운트된 드라이브를 확인하세요.

```sh
ls /mnt/
```
**출력 예시 (정상적인 경우)**
```
c  d  e
```
만약 `e` 드라이브가 보이지 않는다면, **자동 마운트가 비활성화되었거나, Windows에서 드라이브가 감지되지 않은 상태**입니다.

### 🔹 **해결 방법: 수동 마운트**
1. **E 드라이브를 수동 마운트**
   ```sh
   sudo mkdir -p /mnt/e
   sudo mount -t drvfs E: /mnt/e
   ```
   이후 `/mnt/e/`가 정상적으로 접근 가능한지 확인합니다.
   ```sh
   ls /mnt/e/
   ```

2. **만약 마운트 해제 후 다시 마운트하려면**
   ```sh
   sudo umount /mnt/e
   sudo mount -t drvfs E: /mnt/e
   ```

---

## 📌 **2. 자동 마운트 활성화 (`wsl.conf` 설정)**
WSL에서 Windows 드라이브가 자동으로 마운트되지 않는다면, `/etc/wsl.conf` 파일을 수정하여 자동 마운트를 활성화할 수 있습니다.

### 🔹 **설정 파일 편집**
```sh
sudo nano /etc/wsl.conf
```
파일이 없을 경우 새로 생성됩니다.

### 🔹 **자동 마운트 설정 추가**
```ini
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"
```
이후 **WSL을 다시 시작하여 적용**합니다.

```sh
wsl --shutdown
wsl
```

---

## 📌 **3. `/mnt/e/내보내기/` 폴더가 없다고 나오는 경우**
WSL에서 `ls -l /mnt/e/내보내기/` 실행 시 `"No such device"` 오류가 발생하는 경우, Windows에서 해당 드라이브가 정상적으로 연결되었는지 확인해야 합니다.

### 🔹 **해결 방법**
1. **Windows에서 E 드라이브 확인**
   - 파일 탐색기에서 `E:\` 드라이브가 존재하는지 확인
   - `E:\내보내기\` 폴더가 실제로 있는지 확인

2. **Windows에서 E 드라이브 다시 마운트 (관리자 권한)**
   - **PowerShell에서 실행**  
     ```powershell
     Get-Partition -DriveLetter E | Set-Partition -IsOffline $false
     ```
   - WSL에서 다시 마운트  
     ```sh
     sudo mount -t drvfs E: /mnt/e
     ```

3. **WSL에서 `/mnt/e/`를 다시 확인**
   ```sh
   ls -l /mnt/e/
   ```

---

## 📌 **4. WSL이 Windows 드라이브를 읽기 전용으로 마운트하는 경우**
일부 사용자 환경에서 Windows 드라이브가 **읽기 전용(Read-only)** 으로 마운트될 수 있습니다.

### 🔹 **해결 방법**
1. **현재 마운트 옵션 확인**
   ```sh
   mount | grep /mnt/e
   ```
   예제 출력 (읽기 전용인 경우)
   ```
   E: on /mnt/e type drvfs (ro,relatime)
   ```

2. **읽기-쓰기(R/W) 모드로 다시 마운트**
   ```sh
   sudo umount /mnt/e
   sudo mount -t drvfs E: /mnt/e -o rw
   ```

---

## 📌 **5. WSL에서 드라이브 권한 오류 해결**
WSL에서 `/mnt/e/`의 특정 파일이나 폴더를 수정하려고 할 때 **"Permission denied"** 오류가 발생하는 경우, Windows 권한 문제일 가능성이 높습니다.

### 🔹 **해결 방법**
1. **WSL에서 `metadata` 옵션 활성화 후 재부팅**
   `/etc/wsl.conf` 파일을 수정하여 `metadata` 옵션을 활성화합니다.

   ```ini
   [automount]
   enabled = true
   root = /mnt/
   options = "metadata,umask=22,fmask=11"
   ```

2. **WSL을 다시 시작**
   ```sh
   wsl --shutdown
   wsl
   ```

3. **파일 권한 수동 조정**
   ```sh
   sudo chmod -R 777 /mnt/e/내보내기/
   ```

---

## 📌 **6. `/mnt/` 관련 설정이 적용되지 않는 경우**
WSL 설정을 변경했는데도 반영되지 않는다면 **Windows 터미널을 완전히 종료하고 다시 시작**해야 합니다.

### 🔹 **WSL 다시 시작 명령어**
```sh
wsl --shutdown
wsl
```
또는 **Windows 재부팅 후 다시 확인**합니다.

---

## ✅ **최종 정리**
| 문제 | 해결 방법 |
|------|---------|
| `/mnt/e/` 드라이브가 보이지 않음 | `sudo mount -t drvfs E: /mnt/e` |
| `/mnt/e/내보내기/` 접근 불가 | Windows에서 폴더 존재 여부 확인 |
| `No such device` 오류 | Windows에서 드라이브 마운트 확인 후 WSL 재시작 |
| `Permission denied` 오류 | `wsl.conf` 설정 후 `wsl --shutdown` |
| 읽기 전용(ro)로 마운트됨 | `sudo mount -t drvfs E: /mnt/e -o rw` |

🚀 위 설정을 적용하면 `/mnt/e/내보내기/` 경로가 WSL에서 정상적으로 인식될 것입니다.

---

## 📞 문의
- **Software Engineer**: [Seunghak Hong](https://github.com/amirer21)
- **Blog**: [amirer21.github.io](https://amirer21.github.io/)