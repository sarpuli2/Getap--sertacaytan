from main.models import Stajyerinfo
from django.shortcuts import render

def anasayfa_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        userinfo = Stajyerinfo.objects.filter(register__id=user_id).first()
        if userinfo:
            dal = userinfo.dal
            return render(request, 'nvbar/anasayfa.html', {'example': dal})
        else:
            return render(request, 'nvbar/anasayfa.html', {'example': 'Stajyer'})
    else:
        return render(request, 'nvbar/anasayfa.html', {'example': 'Stajyer'})
