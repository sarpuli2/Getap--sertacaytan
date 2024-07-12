from django.utils.deprecation import MiddlewareMixin
from .models import Register

class CustomAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = Register.objects.get(id=user_id)
                request.user = user
            except Register.DoesNotExist:
                request.user = None
        else:
            request.user = None
