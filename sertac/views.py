from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Register, Stajyerinfo
from .forms import Kullaniciveri
from .tokens import hesaponaytoken, passwordreflesh
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from . import utils
from .utils import email_gonderme_SifreIcın
from django.contrib.auth.decorators import login_required


def email_gonderme(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Hesap Aktivasyonu'
    message = render_to_string('email_gonderme.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': hesaponaytoken.make_token(user),
    })
    send_mail(
        mail_subject,
        message,
        'admin@example.com',
        [user.mail],
        fail_silently=False,
    )

def email_gonderme_SifreIcın(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Şifre Yenileme'
    message = render_to_string('email_gonderme_sifreicin.html', {
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
        return redirect('stajyerinfo')
    else:
        return render(request, 'login.html', {'warning': 'Lütfen Emailinizi doğrulayın.'})
    
def passwordchange(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Register.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Register.DoesNotExist):
        user = None
    
    if user is not None and passwordreflesh.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                user.password = password
                user.password2 = password2
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Şifreniz başarıyla değiştirildi.')
                return redirect('login') 
            else:
                return render(request, 'sifreyenileme/changepassword.html', {'warning': 'Şifreler eşleşmiyor.'})
        
 
        return render(request, 'sifreyenileme/changepassword.html', {'uidb64': uidb64, 'token': token})
    
    else:
        return render(request, 'login.html', {'warning': 'Geçersiz istek veya bağlantı süresi aşımı.'})

def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        mail = request.POST['mail']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if Register.objects.filter(mail=mail).exists():
                messages.error(request, 'Böyle bir Email zaten var.')
            else:
                register = Register(name=name, surname=surname, mail=mail, password=password, password2=password2, aktifmi=False)
                register.save()
                messages.success(request, 'Kayıt Başarılı! Hesabınızı onaylamak için Emailinize gelen bağlantıya tıklayınız.')
                email_gonderme(register, request)
                return redirect('login')
        else:
            messages.error(request, 'Şifreler eşleşmiyor!')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        password = request.POST['password']
        
        user = Register.objects.filter(mail=mail, password=password).first()
        if user is not None:
            if user.aktifmi:
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_surname'] = user.surname
                request.session['user_mail'] = user.mail
                request.session['is_authenticated'] = True
                messages.success(request, 'Giriş Başarılı!.')
                return redirect('anasayfa')
            else:
                messages.warning(request, 'Lütfen mailinizi onaylayınız!')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış!')
    
    return render(request, 'login.html')

def stajyerinfo_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user_name = request.session.get('user_name')
    user_surname = request.session.get('user_surname')

    try:
        stajyerinfo_entry = Stajyerinfo.objects.get(user_id=user_id)
        return redirect('update', id=stajyerinfo_entry.id)
    except Stajyerinfo.DoesNotExist:
        if request.method == 'POST':
            form = Kullaniciveri(request.POST, request.FILES)
            if form.is_valid():
                stajyerinfo_entry = form.save(commit=False)
                stajyerinfo_entry.user_id = user_id
                stajyerinfo_entry.name = user_name
                stajyerinfo_entry.save()
                messages.success(request, 'İletişim bilgileri başarıyla kaydedildi.')
                return redirect('stajyerinfo')
            else:
                messages.error(request, 'Form geçerli değil: ' + str(form.errors))
        else:
            form = Kullaniciveri()

        return render(request, 'stajyerinfo.html', {'form': form, 'user_name': user_name, 'user_surname': user_surname})

def update_view(request, id):
    stajyerinfo_entry = get_object_or_404(Stajyerinfo, id=id)
    form = Kullaniciveri(instance=stajyerinfo_entry)
    
    if request.method == 'POST':
        form = Kullaniciveri(request.POST, request.FILES, instance=stajyerinfo_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veri başarıyla güncellendi.')
            return redirect('stajyerinfo')

    return render(request, 'update.html', {'form': form})

def delete_view(request, id):
    obj = get_object_or_404(Stajyerinfo, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Veri başarıyla silindi.')
        return redirect('stajyerinfo')
    return HttpResponse('Silme işlemi başarısız oldu.')

def logout_view(request):
    logout(request)
    return redirect('login')
 
#şifre yenileme sertaç bişiler deniyo

def sendpasswordkey_view(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')  # Bu satırı düzelttik
        user = Register.objects.filter(mail=mail).first()

        if user:
            messages.success(request, 'Email başarılı şekilde gönderildi lütfen mailinizi kontrol ediniz.')
            email_gonderme_SifreIcın(user, request)
            return redirect('login')
        else:
            messages.error(request, 'Böyle bir Email sisteme kayıtlı değil! Lütfen tekrar deneyiniz.')
            return redirect('sendmail')
    else:
        return render(request, 'sifreyenileme/sendmail.html') 
#şifre yenileme django not working

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'registration/password_reset_form.html'
#     email_template_name = 'registration/password_reset_email.html'
#     success_url = reverse_lazy('password_reset_done')

# class CustomPasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'registration/password_reset_done.html'

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'registration/password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')

# class CustomPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'registration/password_reset_complete.html'

#@login_required
def anasayfa_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        userinfo = Stajyerinfo.objects.filter(user_id=user_id).first()
        if userinfo:
            dal = userinfo.dal
            return render(request, 'anasayfa.html', {'example': dal})
        else:
            return render(request, 'anasayfa.html', {'example': 'Stajyer'})
    else:
        return render(request, 'anasayfa.html', {'example': 'Stajyer'})

def profil_view(request):
    user_id = request.session.get('user_id')
    profil_entry = get_object_or_404(Register, id=user_id)
    form = Kullaniciveri(instance=profil_entry)
    
    if request.method == 'POST':
        form = Kullaniciveri(request.POST, instance=profil_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veri başarıyla güncellendi.')
            return redirect('profil')

    return render(request, 'profil.html', {'form': form})