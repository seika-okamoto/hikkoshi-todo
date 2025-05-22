from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task

from collections import defaultdict

@login_required  # ← ログインしてる人だけアクセスできる
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    
     # カテゴリごとにまとめる
    grouped_tasks = defaultdict(list)
    for task in tasks:
        grouped_tasks[task.category].append(task)
    

    return render(request, 'todo/index.html', {'grouped_tasks': grouped_tasks})