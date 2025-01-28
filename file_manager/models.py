from django.db import models
from django.utils.timezone import now


class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소")
    user_agent = models.TextField(verbose_name="디바이스 정보")
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name="방문 시간")

    def __str__(self):
        return f"{self.ip_address} - {self.visit_time}"


class UserActionLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소")
    action_time = models.DateTimeField(default=now, verbose_name="행위 시간")
    action_type = models.CharField(max_length=50, verbose_name="행위 유형")  # 예: 다운로드
    file_names = models.TextField(verbose_name="파일 이름들")  # 다운로드한 파일 이름 저장
    user_agent = models.TextField(verbose_name="디바이스 정보", blank=True)

    def __str__(self):
        return f"[{self.action_time}] {self.ip_address} - {self.action_type}"
