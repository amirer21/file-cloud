from django.db import models

class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소")
    user_agent = models.TextField(verbose_name="디바이스 정보")
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name="방문 시간")

    def __str__(self):
        return f"{self.ip_address} - {self.visit_time}"
