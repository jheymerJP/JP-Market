from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'cuentas'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='register'),
    path('salir/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.profile_view, name='profile'),
    path('editar-perfil/', views.edit_profile_view, name='edit_profile'),
    path('rastrear/<str:order_id>/', views.order_tracking_view, name='order_tracking'),
    path('google/login/', views.google_login, name='google_login'),
]

urlpatterns += [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='cuentas/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='cuentas/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='cuentas/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='cuentas/password_reset_complete.html'),
         name='password_reset_complete'),
]
