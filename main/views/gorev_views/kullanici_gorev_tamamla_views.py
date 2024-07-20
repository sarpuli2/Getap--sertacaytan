from django.shortcuts import render, redirect, get_object_or_404
from main.models import VerilenGorev, TamamlananGorev, Register  # Register modelini import edin
from django.contrib import messages

def gorev_tamamla_views(request, gorev_id):
    gorev = get_object_or_404(VerilenGorev, id=gorev_id)
    
    if request.method == 'POST':
        description = request.POST.get('description')
        file = request.FILES.get('file')
        github_link = request.POST.get('github_link')
        
        tamamlanan_gorev = TamamlananGorev(
            gorev=gorev,
            user=Register.objects.get(id=request.session['user_id']),
            description=description,
            file=file,
            github_link=github_link
        )
        tamamlanan_gorev.save()
        
        user = Register.objects.get(id=request.session['user_id'])
        user.completed_tasks += 1
        user.save()
        
        gorev.assigned_to.remove(user)
        
        messages.success(request, 'Görev başarıyla tamamlandı.')
        return redirect('kullanicigorevler', user_id=request.session['user_id'])

    return render(request, 'gorev/gorevtamamla.html', {'gorev': gorev})
