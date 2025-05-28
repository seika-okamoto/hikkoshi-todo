from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='home'),
    path('set_move_date/', views.set_move_date, name='set_move_date'),
]
