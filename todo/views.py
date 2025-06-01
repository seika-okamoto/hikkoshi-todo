from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from collections import defaultdict
from django.views.decorators.http import require_POST
from .models import Task, Category 
import datetime
from django.utils import timezone

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

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    new_title = request.POST.get('title')
    if new_title:
        task.title = new_title
        task.save()
    return redirect('todo:edit')

@require_POST
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('todo:edit')

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        memo = request.POST.get('memo')  
        category_id = request.POST.get('category')
        deadline_option = request.POST.get('deadline')
        category = Category.objects.get(id=category_id) if category_id else None

        # 今日を基準に締め切り日を計算
        today = timezone.now().date()

        if deadline_option == '1month_before':
            due_date = today - datetime.timedelta(weeks=4)
        elif deadline_option == '3weeks_before':
            due_date = today - datetime.timedelta(weeks=3)
        elif deadline_option == '2weeks_before':
            due_date = today - datetime.timedelta(weeks=2)
        elif deadline_option == '1week_before':
            due_date = today - datetime.timedelta(weeks=1)
        elif deadline_option == 'on_the_day':
            due_date = today
        elif deadline_option == '2weeks_after':
            due_date = today + datetime.timedelta(weeks=2)
        else:
            due_date = None  # 万が一
        
        Task.objects.create(
            user=request.user,
            title=title,
            memo=memo,  
            category=category,
            due_date=due_date 
        )

        return redirect('todo:index')

    else:
        categories = Category.objects.all()
        return render(request, 'todo/add.html', {'categories': categories, 'hide_header': True})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    # 必要に応じてメモとコメントも取得（これから作る！）
    # 例:
    # memos = Memo.objects.filter(task=task)
    # comments = Comment.objects.filter(task=task)

    return render(request, 'todo/task_detail.html', {
        'task': task,
        # 'memos': memos,
        # 'comments': comments,
        'hide_header': True  # 必要ならナビ非表示
    })
