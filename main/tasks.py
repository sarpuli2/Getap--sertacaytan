from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from main.models import Register
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from main.tokens import hesaponaytoken, passwordreflesh

@shared_task
def email_gonderme(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Hesap Aktivasyonu'
    message = render_to_string('mailgonderme/email_gonderme.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': hesaponaytoken.make_token(user),
    })
    send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL
        [user.mail],
        fail_silently=False,
    )

@shared_task
def email_gonderme_SifreIcın(user_id, domain):
    user = Register.objects.get(id=user_id)
    mail_subject = 'Şifre Sıfırlama'
    message = render_to_string('mailgonderme/email_gonderme_sifreicin.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': passwordreflesh.make_token(user),
    })
    send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.mail],
        fail_silently=False,
    )

@shared_task
def deactivate_user(user_id):
    try:
        user = Register.objects.get(id=user_id)
        user.aktifmi = False
        user.save()
    except Register.DoesNotExist:
        pass

