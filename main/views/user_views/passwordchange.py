from django.utils.http import urlsafe_base64_decode
from main.tokens import passwordreflesh
from main.models.Register import Register
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password

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
                if check_password(password, user.password):
                    messages.warning(request, 'Şifreniz bir önceki şifreyle aynı olamaz!')
                    return render(request, 'sifreyenileme/changepassword.html', {'uidb64': uidb64, 'token': token})
                else:
                    user.password = password
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Şifreniz başarıyla değiştirildi.')
                    return redirect('login')
            else:
                messages.warning(request, 'Şifreler eşleşmiyor.')
                return render(request, 'sifreyenileme/changepassword.html', {'uidb64': uidb64, 'token': token})

        return render(request, 'sifreyenileme/changepassword.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.warning(request, 'Geçersiz istek veya bağlantı süresi aşımı.')
        return render(request, 'nvbar/login.html')
