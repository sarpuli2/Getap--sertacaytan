from django.urls import path
from main.views import *
from main.views.nvbar_views.logout_view import logout_view
from main.views.nvbar_views.stajyerinfo_view import stajyerinfo_view
from main.views.user_views.sendpasswordkey_view import sendpasswordkey_view
from main.views.user_views.user_profile_detail_views import user_profile_detail_views
from django.conf.urls.static import static
from django.conf import settings
#from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', anasayfa_view, name='anasayfa'),
    #kayıt-giriş
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    #nvbar
    path('anasayfa/', anasayfa_view, name='anasayfa'),
    path('stajyerinfo/', stajyerinfo_view, name='stajyerinfo'),
    path('profil/', profil_view, name='profil'),
    #crud
    path('update/<int:id>/', update_view, name='update'),
    path('delete/<int:id>/', delete_view, name='delete'),
    #şifre yenileme 
    path('sendmail/', sendpasswordkey_view, name='sendmail'),
    #aktifleme tokenli
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('passwordchange/<uidb64>/<token>/', passwordchange, name='passwordchange'),
    #kullanıcı yönetim
    path('users/', users_views, name='users_list'),
    path('userdetail/<int:id>/', user_profile_detail_views, name='user_profile_detail'),
    path('users/<int:user_id>/', user_detail_views, name='user_detail'), 
    path('users/delete/<int:user_id>/', user_delete, name='user_delete'), 



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)