from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from main.models import Register
from main.tasks import email_gonderme_SifreIcın

def sendpasswordkey_view(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        user = Register.objects.filter(mail=mail).first()

        if user:
            domain = get_current_site(request).domain
            email_gonderme_SifreIcın(user.id, domain)
            messages.success(request, 'Email başarılı şekilde gönderildi, lütfen mailinizi kontrol ediniz.')
            return redirect('login')
        else:
            messages.error(request, 'Böyle bir Email sisteme kayıtlı değil! Lütfen tekrar deneyiniz.')
            return redirect('sendmail')
    else:
        return render(request, 'sifreyenileme/sendmail.html')
