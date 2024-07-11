from django.urls import path
from .views import register_view, login_view, anasayfa_view, activate, passwordchange
from . import views
from django.conf.urls.static import static
from django.conf import settings
#from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('', login_view, name='login'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('anasayfa/', anasayfa_view, name='anasayfa'),
    path('update/<int:id>/', views.update_view, name='update'),
    path('delete/<int:id>/', views.delete_view, name='delete'),
    path('logout/', views.logout_view, name='logout'),
    #şifre yenileme sertaç bişiler deniyor;
    path('sendmail/', views.sendpasswordkey_view, name='sendpasswordkey_view'),
    path('passwordchange/<uidb64>/<token>/', passwordchange, name='passwordchange'),


    #şifremi unuttum kısmı django;
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)