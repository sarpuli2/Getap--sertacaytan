from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import AnonymousUser
from .models import Register  # assuming Register model is in models.py

class CustomAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        super().process_request(request)  # Call the parent process_request method

        user_id = request.session.get('_auth_user_id')
        if user_id:
            try:
                user = Register.objects.get(id=user_id)
                request.user = user
            except Register.DoesNotExist:
                request.user = AnonymousUser()  # set request.user to AnonymousUser
        else:
            request.user = AnonymousUser()  # set request.user to AnonymousUser
