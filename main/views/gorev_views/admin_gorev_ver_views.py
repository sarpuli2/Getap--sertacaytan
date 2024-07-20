from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import Register, VerilenGorev

def admin_gorev_ver_views(request):
    kullanicilar = Register.objects.filter(aktifmi=True)
    
    if request.method == 'POST':
        taskname = request.POST.get('taskname')
        taskcontent = request.POST.get('taskcontent')
        taskimage = request.FILES.get('taskimage')
        taskfile = request.FILES.get('taskfile')
        selected_users = request.POST.getlist('selected_users')

        if request.session.get('is_authenticated'):
            assigned_by = Register.objects.get(id=request.session['user_id'])
        else:
            messages.error(request, 'Görev atamak için oturum açmanız gerekiyor.')
            return redirect('login')

        verilengorev = VerilenGorev(
            taskname=taskname, 
            taskcontent=taskcontent, 
            taskimage=taskimage, 
            taskfile=taskfile, 
            assigned_by=assigned_by  
        )
        verilengorev.save()

        for user_id in selected_users:
            user = Register.objects.get(id=user_id)
            verilengorev.assigned_to.add(user)

        verilengorev.save()

        if verilengorev.id:
            messages.success(request, 'Görev başarıyla verildi.')
        else:
            messages.error(request, 'Görev verilemedi, lütfen tekrar deneyin.')

        return redirect('kullanicigorevler', user_id=request.session['user_id'])
    
    return render(request, 'gorev/admingorevdetay.html', {'kullanicilar': kullanicilar})
