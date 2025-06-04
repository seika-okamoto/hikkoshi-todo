from django.urls import path
from . import views

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
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment')
]