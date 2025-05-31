from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from collections import defaultdict
from django.views.decorators.http import require_POST

@require_POST
@login_required  # ← ログインしてる人だけアクセスできる
def toggle_done(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = not task.is_done  # チェックをトグル
    task.save()
    return redirect('todo:index')

def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('category','due_date')
        
    # grouped_tasks を最初に定義
    grouped_tasks = defaultdict(list)
    
     # カテゴリごとにまとめる
    for task in tasks:
        grouped_tasks[task.category.name].append(task)

    # 件数の計算
    total_count = tasks.count()
    done_count = tasks.filter(is_done=True).count()
    if total_count > 0:
        done_rate = round((done_count / total_count) * 100, 1)  # 小数点1桁まで
    else:
        done_rate = 0

    return render(request, 'todo/index.html', {
        'grouped_tasks': dict(grouped_tasks),
        'total_count': total_count,
        'done_count': done_count,
        'done_rate': done_rate
    })

@login_required
def edit_todo(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/edit.html', {'tasks': tasks})

