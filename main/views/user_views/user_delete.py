from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from main.models import Register

def user_delete(request, user_id):
    user = get_object_or_404(Register, pk=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Kullanıcı başarıyla silindi.')
        return redirect('/users/')  # /users/ URL'ine yönlendirme

    # Eğer GET isteği yapılmışsa, silme işlemine onay sayfası gibi bir şey göstermeyin
    return redirect('/users/')  # Silme işlemi onay sayfası olmadan doğrudan yönlendirme
