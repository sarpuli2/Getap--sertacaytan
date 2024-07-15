from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
import six
from main.models import Register

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.aktifmi)
        )

    def make_token(self, user):
        signer = TimestampSigner()
        token = super().make_token(user)
        signed_token = signer.sign(token)
        return signed_token

    def check_token(self, user, token, max_age=3600):  # max_age is in seconds, e.g., 3600 seconds = 1 hour
        signer = TimestampSigner()
        try:
            token = signer.unsign(token, max_age=max_age)
        except (BadSignature, SignatureExpired):
            return False
        return super().check_token(user, token)

hesaponaytoken = AccountActivationTokenGenerator()

class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + user.password + six.text_type(timestamp)
        )

    def make_token(self, user):
        signer = TimestampSigner()
        token = super().make_token(user)
        signed_token = signer.sign(token)
        return signed_token

    def check_token(self, user, token, max_age=3600):  # max_age is in seconds, e.g., 3600 seconds = 1 hour
        signer = TimestampSigner()
        try:
            token = signer.unsign(token, max_age=max_age)
        except (BadSignature, SignatureExpired):
            return False
        return super().check_token(user, token)

passwordreflesh = CustomPasswordResetTokenGenerator()


