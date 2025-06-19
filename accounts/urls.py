from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import CustomPasswordResetView 
from .views import CustomPasswordResetCompleteView


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
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        extra_context={'hide_header': True}  
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('accounts:password_reset_complete'),
        extra_context={'hide_header': True}
    ), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/', CustomPasswordResetView.as_view(
    success_url=reverse_lazy('accounts:password_reset_done'),
    email_template_name='registration/password_reset_email.html',
    extra_context={'hide_header': True}
    ), name='password_reset'),
    path('about/', views.about_app, name='about_app'),

]