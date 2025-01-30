### **📌 Release Note - Django File Manager 🚀**  

**📅 Release Date:** 2025-01-30  
**🛠️ Version:** 1.0.0  

---

## **🎯 목표 (Goal)**  
- 사용자 친화적인 웹 기반 파일 관리 시스템 구축  
- NEF 원본 이미지를 JPG로 변환하여 미리보기 제공  
- 파일 다운로드 기능 추가  
- **WSL + Django + Nginx 배포**  
- **카카오톡 로그인 API를 통한 인증 및 접근 보안 강화**  
- **외부 네트워크에서 안전하게 Django 서버 접근 가능하도록 포트 포워딩 및 리버스 프록시 적용**  

---

## **📌 주요 기능 (Key Features)**  

### **✅ Version 1.0.0 (Initial Release)**  
**🎯 목표:** Django 기반 파일 관리 웹 서비스 구축  

#### **1️⃣ 프로젝트 환경 설정**  
- Django 프로젝트 & 앱 생성 (`file_manager`)  
- WSL2 기반 가상 환경 구성 (`venv` 사용)  
- MySQL 연결 및 데이터베이스 마이그레이션  
- `.env` 파일을 이용한 환경변수 설정  

#### **2️⃣ 파일 미리보기 및 다운로드 기능**  
- `/media/` 경로에서 미리보기 이미지 제공  
- `/download/<file_name>/` 경로에서 다운로드 가능  

#### **3️⃣ UI 개선**  
- `file_list.html`에서 썸네일 기반의 파일 목록 표시  
- 다운로드 버튼 추가  


#### **4️⃣ 서버 접근 가능하도록 포트 포워딩 설정**  
- **공유기 포트 포워딩**: 외부 IP(`175.208.213.7`) → 내부 WSL IP (`172.26.213.34:8088`)  
- **WSL2 네트워크 설정**: `netsh interface portproxy` 사용하여 80번 포트 매핑  
- **UFW 방화벽 설정**: `80`, `8088` 포트 허용  


### **✅ Version 1.0.1 **  
#### **1️⃣ 카카오 로그인 API 연동**  
- `social-auth-app-django`를 활용한 OAuth 2.0 인증  
- `/login/` URL을 카카오 로그인 페이지로 리디렉션  
- 로그인 성공 시 `/download-list/`로 이동  
- `social_auth_usersocialauth` 테이블을 활용한 사용자 계정 연동  
- `kakao_account` API를 통해 이메일 및 프로필 정보 저장  


---

### **✅ Version 1.0.2 (Deployment & Optimization)**  
**🎯 목표:** Django 프로젝트 배포 및 성능 최적화  

#### **1️⃣ Nginx 배포**  
- **Nginx 리버스 프록시 설정**: `80`번 포트 요청을 `127.0.0.1:8088`로 전달  
- `/media/`, `/static/` 정적 파일 서빙 지원 (`location /static/ {}` 설정)  

#### **2️⃣ 외부 접속 지원**  
- **포트 포워딩 설정** (공유기에서 `80`번 포트를 내부 WSL IP(`172.26.213.34:8088`)로 연결)  
- **도메인 DNS 설정**: `A 레코드`를 `175.208.213.7`로 설정하여 `devmiro.co.kr`과 연결  

#### **3️⃣ 버그 수정 및 성능 개선**  
- `403 Forbidden` 오류 해결 (Nginx 권한 문제)  
- `/media/` 정적 파일 로드 개선  
- WSL에서 Windows 파일 접근 (`/mnt/e/...`) 최적화  

#### **4️⃣ 카카오 로그인 안정화**  
- **Redirect URI 오류 (`KOE006`) 해결**  
- `settings.py`에서 `SOCIAL_AUTH_KAKAO_SCOPE` 추가 (`profile`, `account_email`)  
- `/logout/` URL 추가하여 카카오 로그아웃 기능 지원  

---


### **✅ Version 1.0.3 (Visitor Logs & GeoIP2 Integration)**
**🎯 목표:** 방문자 추적 기능 강화 및 GeoIP2 기반 위치 정보 추가  

#### **1️⃣ 방문자 로그(VisitorLog) 기능 확장**  
- 기존 **IP 주소 및 User-Agent 정보** 저장 기능에서 **추가 필드** 지원  
- 새로운 **로그 필드 추가**:  
  - `browser`: 방문자의 브라우저 정보  
  - `operating_system`: 방문자의 OS 정보  
  - `country`: GeoIP2를 사용한 국가 정보  
  - `city`: GeoIP2를 사용한 도시 정보  
  - `referer_url`: 사용자가 어디에서 왔는지 추적  
  - `request_url`: 방문한 경로  
  - `http_method`: GET/POST 등의 요청 방식  
  - `session_id`: Django 세션을 활용한 방문자 식별  

#### **2️⃣ GeoIP2 데이터베이스 적용**  
- **GeoLite2 데이터베이스**를 이용하여 **방문자의 국가 및 도시 정보 자동 저장**  
- `pip install maxminddb-geolite2` 패키지 추가  
- `/usr/share/GeoIP/GeoLite2-City.mmdb` 데이터베이스 설정 (`settings.py` 반영)  
- `8.8.8.8`, `1.1.1.1` 같은 공인 IP로 국가/도시 정보 테스트 가능  

#### **3️⃣ 프록시 환경 고려한 클라이언트 IP 추출 개선**  
- 기존 `get_client_ip()` 함수에서 `X-Forwarded-For`와 `X-Real-IP` 지원 추가  
- 사설 IP(`172.x.x.x`, `192.168.x.x`)의 경우 `"Private Network"`로 기록하여 구분  

#### **4️⃣ WSL에서 `/mnt/` 관련 문제 해결**  
- WSL에서 `E:` 드라이브가 자동 마운트되지 않는 문제 해결  
- `/etc/wsl.conf` 파일 수정하여 **자동 마운트 활성화**  
  ```ini
  [automount]
  enabled = true
  root = /mnt/
  options = "metadata,umask=22,fmask=11"
  ```
- `sudo mount -t drvfs E: /mnt/e` 명령어 추가  
- WSL 종료 후 재시작 (`wsl --shutdown && wsl`)  

---

### **✅ 버그 수정 및 성능 개선**  
- `request_url` 필드 추가 시 **마이그레이션 기본값 설정 오류 해결**  
- `/mnt/e/내보내기/` 경로 오류 해결을 위한 `wsl.conf` 설정 가이드 포함  
- **세션 ID 기록을 통해 동일 방문자 세션 추적 가능**  

---

## **📈 향후 계획 (Backlog)**  
✅ **Version 1.0.4** (UI 개선 및 사용자 기능 추가)  
🔹 파일 정렬 및 필터 기능 추가  
🔹 검색 기능 추가  
🔹 **카카오톡 친구 목록 API 활용하여 특정 사용자만 다운로드 가능하도록 제한**  
🔹 **RESTful API 지원 (파일 업로드 및 다운로드 API 제공)**  
🔹 방문자 로그 검색 및 필터 기능 추가  
🔹 관리자 페이지에서 **방문자 기록 대시보드** 제공  
🔹 `/mnt/` 디렉토리 접근 개선 및 자동화 스크립트 추가  


---

## **📢 주의 사항 (Known Issues)**  
⚠️ 대량 파일 다운로드 시 속도 저하 가능성 → **Gzip 압축 및 비동기 다운로드 고려**  
⚠️ `social_auth_usersocialauth` 테이블이 없을 경우 `python manage.py migrate` 실행 필요  
⚠️ **WSL2의 내부 IP가 변경될 경우, 포트 포워딩 설정을 재설정해야 할 수도 있음**  

---

### ✨ **업데이트된 내용:**  
✅ **카카오 로그인 API 인증 흐름 추가**  
✅ **OAuth 2.0 기반 로그인 & 세션 처리 설명 보강**  
✅ **카카오톡 친구 API 연동 계획 추가**  
✅ **Redirect URI 설정 및 KOE006 오류 해결 방안 포함**  
✅ **포트 포워딩 및 공유기 네트워크 설정 추가**  
✅ **Nginx 설정에서 정적 파일 제공 최적화 내용 추가**  

---

### **🏁 결론**  
이 버전은 Django 기반의 파일 관리 웹 애플리케이션을 **완전한 기능 상태**로 배포하기 위한 초기 릴리스입니다. 🎉  
추후 **성능 최적화 & 기능 개선**을 지속적으로 진행할 예정입니다! 🚀  

---

**📝 email:** [amirer21@gmail.com]  
**📅 작성일:** 2025-01-30  