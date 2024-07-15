from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from main.tokens import passwordreflesh

def email_gonderme_SifreIcın(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Şifre Yenileme'
    message = render_to_string('mailgonderme/email_gonderme_sifreicin.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': passwordreflesh.make_token(user),
    })
    send_mail(
        mail_subject,
        message,
        'admin@example.com',
        [user.mail],
        fail_silently=False,
    )
