import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.timezone import now

class AutoLogoutMiddleware:
    """ 일정 시간 동안 활동이 없으면 자동 로그아웃하는 미들웨어 """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get("last_activity")
            if last_activity:
                last_activity = datetime.datetime.fromisoformat(last_activity)
                # 현재 시간과 마지막 활동 시간 비교
                if (now() - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                    logout(request)  # 로그아웃 처리
                    del request.session["last_activity"]  # 세션 삭제
            request.session["last_activity"] = now().isoformat()
        
        response = self.get_response(request)
        return response
