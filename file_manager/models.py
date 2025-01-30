from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소")
    user_agent = models.TextField(verbose_name="디바이스 정보")
    browser = models.CharField(max_length=100, verbose_name="브라우저", blank=True)
    operating_system = models.CharField(max_length=100, verbose_name="운영체제", blank=True)
    country = models.CharField(max_length=50, verbose_name="접속 국가", blank=True)
    city = models.CharField(max_length=100, verbose_name="접속 도시", blank=True)
    referer_url = models.URLField(verbose_name="리퍼러 URL", blank=True, null=True)
    request_url = models.TextField(verbose_name="요청한 URL")
    http_method = models.CharField(max_length=10, verbose_name="요청 메서드", default="GET")
    session_id = models.CharField(max_length=100, blank=True, verbose_name="세션 ID")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="사용자")
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name="방문 시간")

    def __str__(self):
        return f"{self.ip_address} - {self.browser} - {self.visit_time}"


class UserActionLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소")
    action_time = models.DateTimeField(default=now, verbose_name="행위 시간")
    action_type = models.CharField(max_length=50, verbose_name="행위 유형")  # 예: 다운로드
    file_names = models.TextField(verbose_name="파일 이름들")  # 다운로드한 파일 이름 저장
    user_agent = models.TextField(verbose_name="디바이스 정보", blank=True)
    browser = models.CharField(max_length=100, verbose_name="브라우저", blank=True)
    operating_system = models.CharField(max_length=100, verbose_name="운영체제", blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="사용자")
    session_id = models.CharField(max_length=100, blank=True, verbose_name="세션 ID")

    def __str__(self):
        return f"[{self.action_time}] {self.ip_address} - {self.action_type}"
