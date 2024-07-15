from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from main.models import Stajyerinfo
from django.http import HttpResponse

def delete_view(request, id):
    try:
        obj = get_object_or_404(Stajyerinfo, register__id=id)
    except:
        messages.error(request, 'Veri bulunamadı veya zaten silinmiş.')
        return redirect('stajyerinfo') 

    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Veri başarıyla silindi.')
        return redirect('stajyerinfo')

    return HttpResponse('Silme işlemi başarısız oldu.')
