### README.md

```markdown
# Dev Hong Cloud

## 📌 프로젝트 개요
**Dev Hong Cloud**는 이미지 파일을 관리하고, 다운로드하며, 갤러리로 구성된 웹 애플리케이션입니다. 사용자는 카테고리별로 이미지를 확인하고, 선택한 이미지를 ZIP 파일로 다운로드할 수 있습니다. 또한, 방문자 및 사용자 로그를 기록하고 관리하는 기능이 포함되어 있습니다.

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
- **Authentication**: Django Allauth (카카오톡 로그인)
- **Deployment**: 

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

## 🌟 주요 URL
- **갤러리 페이지**: `http://127.0.0.1:8000/gallery/`
- **파일 다운로드 페이지**: `http://127.0.0.1:8000/download-list/`
- **방문자 로그 페이지**: `http://127.0.0.1:8000/visitor-logs/`

---

## 📋 데이터베이스 모델
### 1. **VisitorLog**
방문자 정보를 기록하는 모델.
| 필드          | 설명            |
|---------------|-----------------|
| `ip_address`  | 방문자의 IP 주소 |
| `user_agent`  | 디바이스 정보    |
| `visit_time`  | 방문 시간        |

### 2. **UserActionLog**
사용자의 행동을 기록하는 모델.
| 필드            | 설명                       |
|-----------------|--------------------------|
| `ip_address`    | 사용자 IP 주소             |
| `action_type`   | 액션 타입 (예: Download)    |
| `file_names`    | 다운로드한 파일 목록        |
| `user_agent`    | 디바이스 정보              |
| `action_time`   | 액션 발생 시간             |

---

## 📞 문의
- **Software Engineer**: [Seunghak Hong](https://github.com/amirer21)
- **Blog**: [amirer21.github.io](https://amirer21.github.io/)
```