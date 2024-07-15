from django.utils.http import urlsafe_base64_decode
from main.models.Register import Register
from main.tokens import hesaponaytoken
from django.contrib import messages
from django.shortcuts import render, redirect

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Register.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Register.DoesNotExist):
        user = None

    if user is not None and hesaponaytoken.check_token(user, token):
        user.aktifmi = True

        user.save()
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        request.session['user_surname'] = user.surname
        request.session['user_mail'] = user.mail
        messages.success(request, 'Aktivasyon Başarılı Lütfen Giriş Yapınız.')
        return redirect('login')
    else:
        return render(request, 'nvbar/login.html', {'warning': 'Lütfen Emailinizi doğrulayın.'})