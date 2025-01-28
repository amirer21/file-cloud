from django.test import TestCase, Client
from django.urls import reverse
from file_manager.models import VisitorLog, UserActionLog
from django.contrib.auth.models import User

class FileManagerViewTests(TestCase):
    def setUp(self):
        """테스트 초기 설정"""
        self.client = Client()
        
        # 테스트 사용자 생성 및 로그인
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # URL 설정
        self.gallery_url = reverse('gallery')  # gallery 뷰의 URL
        self.download_list_url = reverse('protected_download_list')  # 다운로드 리스트 URL
        self.download_selected_url = reverse('download_selected')  # POST 요청 테스트 URL

    def test_gallery_view(self):
        """gallery 뷰의 상태 코드 테스트"""
        response = self.client.get(self.gallery_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "file_manager/gallery.html")

    def test_download_list_view(self):
        """다운로드 리스트 뷰 상태 코드 테스트"""
        response = self.client.get(self.download_list_url)
        # 로그인 후 접근 가능하도록 설정했으므로 로그인 후 200 상태 코드 확인
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "file_manager/file_list.html")

    def test_download_selected_post(self):
        """선택된 파일 다운로드 테스트"""
        # 샘플 데이터를 설정합니다.
        selected_images = [
            "4waves/DSC_6603.jpg",
            "hoon/DSC_6197.jpg",
        ]

        # POST 요청 테스트
        response = self.client.post(
            self.download_selected_url,
            {"selected_images": selected_images},
        )

        self.assertEqual(response.status_code, 200)  # 성공적으로 응답을 반환
        self.assertEqual(response["Content-Type"], "application/zip")  # ZIP 파일 확인
        self.assertTrue(response.has_header("Content-Disposition"))
        self.assertIn("selected_images.zip", response["Content-Disposition"])

    def test_log_visitor(self):
        """방문자 로그 저장 테스트"""
        self.client.get(self.gallery_url)

        # VisitorLog 모델에 로그가 저장되었는지 확인
        self.assertEqual(VisitorLog.objects.count(), 1)
        visitor_log = VisitorLog.objects.first()
        self.assertIsNotNone(visitor_log.ip_address)
        self.assertIsNotNone(visitor_log.user_agent)
        self.assertEqual(visitor_log.ip_address, "127.0.0.1")  # 테스트 클라이언트의 IP는 항상 로컬호스트

    def test_user_action_log(self):
        """사용자 액션 로그 테스트"""
        selected_images = [
            "4waves/DSC_6603.jpg",
            "hoon/DSC_6197.jpg",
        ]

        # POST 요청으로 파일 다운로드 시 액션 로그가 저장되는지 확인
        self.client.post(self.download_selected_url, {"selected_images": selected_images})

        # UserActionLog 모델 확인
        self.assertEqual(UserActionLog.objects.count(), 1)
        action_log = UserActionLog.objects.first()
        self.assertEqual(action_log.action_type, "Download")
        self.assertIn("4waves/DSC_6603.jpg", action_log.file_names)
        self.assertIn("hoon/DSC_6197.jpg", action_log.file_names)

    def test_no_files_selected(self):
        """선택된 파일이 없을 때의 응답 테스트"""
        response = self.client.post(self.download_selected_url, {"selected_images": []})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "No files selected.")
