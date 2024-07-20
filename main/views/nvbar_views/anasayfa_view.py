from main.models import Stajyerinfo, Register
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login

def anasayfa_view(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    user_surname = request.session.get('user_surname')
    image = request.session.get('image', 'profileimages/default/defaultphotoforstajyer.jpg')
    is_authenticated = request.session.get('is_authenticated', False)
    user_yetki = request.session.get('user_yetki', 'Stajyer')

    example = 'Stajyer'  # Varsayılan değer

    if user_id:
        userinfo = Stajyerinfo.objects.filter(register__id=user_id, register__image=image).first()
        if userinfo:
            example = userinfo.dal

    return render(request, 'nvbar/anasayfa.html', {
        'example': example,
        'user_name': user_name,
        'user_surname': user_surname,
        'image': image,
        'is_authenticated': is_authenticated,
        'user_yetki': user_yetki
    })
