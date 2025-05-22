from django.conf import settings

class HiddenMethodOverrideMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and "_method" in request.POST:
            override_method = request.POST["_method"]
            if override_method in ["PUT", "PATCH", "DELETE"]:
                request.method = override_method
                request.META["REQUEST_METHOD"] = override_method
                csrf_token = request.COOKIES.get(settings.CSRF_COOKIE_NAME)
                request.META[settings.CSRF_HEADER_NAME] = csrf_token
        return self.get_response(request)
