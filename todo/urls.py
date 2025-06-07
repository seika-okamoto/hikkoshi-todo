from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.task_list, name='index'), 
    path('toggle_done/<int:task_id>/', views.toggle_done, name='toggle_done'),   
    path('edit/', views.edit_todo, name='edit'),  
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('add/', views.add_task, name='add_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/add_memo/', views.add_memo, name='add_memo'),
    path('task/<int:task_id>/add_comment/', views.add_comment, name='add_comment'),
    path('like/<int:comment_id>/', views.toggle_like, name='toggle_like'),
    path('share_items/', views.share_items, name='share_items'),
    path('toggle_done_ajax/<int:task_id>/', views.toggle_done_ajax, name='toggle_done_ajax'),

]

