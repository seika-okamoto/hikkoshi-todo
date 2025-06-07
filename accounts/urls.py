from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('edit_username/', views.edit_username, name='edit_username'),
    path('edit_email/', views.edit_email, name='edit_email'),
    path('email_change_sent/', views.email_change_sent, name='email_change_sent'),
    path('confirm_email_change/<uuid:token>/', views.confirm_email_change, name='confirm_email_change'),
    path('change_password/', views.change_password, name='change_password'),
    path('comment_history/', views.comment_history, name='comment_history'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    # ✅ password reset 関連
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
        extra_context={'hide_header': True}  
        ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        success_url=reverse_lazy('accounts:password_reset_done'),
        email_template_name='accounts/password_reset_email.html'  # ← 追加
    ), name='password_reset'),
    path('about/', views.about_app, name='about_app'),
    path('resend_email/', views.resend_email, name='resend_email'),
]