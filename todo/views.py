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
    
    print(f"✅ ログインユーザー: {request.user}")
    print(f"✅ ユーザーのタスク件数: {tasks.count()}")
    
    # grouped_tasks を最初に定義
    grouped_tasks = defaultdict(list)
    
    for t in tasks:
        print(f"✅ タスク: {t.title}, {t.category}")

     # カテゴリごとにまとめる
    for task in tasks:
        grouped_tasks[task.category].append(task)

    print("✅ grouped_tasks (最終状態):", grouped_tasks)  # 変換後の状態も確認
    
    return render(request, 'todo/index.html', {'grouped_tasks': dict(grouped_tasks)})  # ← `dict()` に変換


