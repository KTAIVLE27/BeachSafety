from django.http import HttpResponseForbidden

class RoleBasedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.role_paths = {
            'control': ['admin', 'supervisor'],
            'adminpanel': ['admin'],
        }

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 각 URL 경로에 따라 필요한 권한 확인
        for path, roles in self.role_paths.items():
            if path in request.path:
                role = getattr(request.user, 'user_role', None)
                if role not in roles:
                    return HttpResponseForbidden(f"You do not have permission to access this page on {path}.")
        
        return self.get_response(request)

