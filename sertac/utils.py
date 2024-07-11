# utils.py

from django.core.mail import send_mail
from django.conf import settings

def email_gonderme_SifreIcın(user, request):
    try:
        subject = 'Şifre Sıfırlama'
        message = 'Şifre sıfırlama bağlantınız: ...'
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.mail]
        
        send_mail(subject, message, from_email, to_list)
    except Exception as e:
        print(f"Email gönderim hatası: {e}")
        # Daha iyi hata yönetimi yapabilirsiniz.
