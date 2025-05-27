from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.task_list, name='index'), 
path('toggle_done/<int:task_id>/', views.toggle_done, name='toggle_done'),   
]

