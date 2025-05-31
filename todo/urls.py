from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.task_list, name='index'), 
    path('toggle_done/<int:task_id>/', views.toggle_done, name='toggle_done'),   
    path('edit/', views.edit_todo, name='edit'),  
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
]

