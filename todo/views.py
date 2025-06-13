from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.views.decorators.http import require_POST
from todo.models import Task, Category, Memo, Comment
import datetime
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from todo.models import Comment, Like, Memo, Task
from django.http import JsonResponse
import json


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
        'done_rate': done_rate,
        'hide_header': True,
    })

@login_required
def edit_todo(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/edit.html', {
        'tasks': tasks,
        'hide_header': True  
        })

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    new_title = request.POST.get('title')
    
    if new_title:
        task.title = new_title
        task.save()

    # 🔑 new_titleがなくてもtasksを定義しておく！
    tasks = Task.objects.filter(user=request.user)

    return render(request, 'todo/edit.html', {
        'tasks': tasks,
        'hide_header': True  
    })

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
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, is_template=True)  # ✅ 雛形限定！

    view = request.GET.get('view', 'memo')
    memos = Memo.objects.filter(task=task).order_by('-created')
    comments = Comment.objects.filter(task=task).order_by('-created_at')

    return render(request, 'todo/task_detail.html', {
        'task': task,
        'view': view,
        'memos': memos,
        'comments': comments,
        'hide_header': True
    })

@login_required
def add_memo(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    context = request.POST.get('context')

    if context:
        Memo.objects.create(
            task=task,
            user=request.user,
            context=context
        )

    return redirect('todo:task_detail', task_id=task.id)

@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id, is_template=True)  # ✅ 雛形だけ対象！

    content = request.POST.get('content')
    display_name = request.POST.get('display_name', 'nickname')

    if content:
        Comment.objects.create(
            task=task,
            user=request.user,
            content=content,
            display_name=display_name
        )

    return redirect(f"{reverse('todo:task_detail', args=[task.id])}?view=comment")

@require_POST
@login_required
def comment_list(request, task_id):
    task = get_object_or_404(Task, id=task_id, is_template=True)  # ✅ 雛形だけ表示

    sort = request.GET.get('sort', 'newest')
    comments = Comment.objects.filter(task=task)

    if sort == 'popular':
        comments = comments.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    else:
        comments = comments.order_by('-created_at')

    context = {
        'task': task,
        'comments': comments,
        'comment_count': comments.count(),
        'sort': sort,
    }
    return render(request, 'todo/comment_list.html', context)

@login_required
def share_items(request):
    incomplete_tasks = Task.objects.filter(user=request.user, is_done=False)

    return render(request, 'todo/share_items.html', {
        'tasks': incomplete_tasks,
        'hide_header': True,
    })

@require_POST
def toggle_done_ajax(request, task_id):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        data = json.loads(request.body)
        task.is_done = data.get('is_done', False)
        task.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'unauthorized'}, status=401)

@login_required
def edit_memo(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)

    if request.method == 'POST':
        new_context = request.POST.get('context')
        memo.context = new_context
        memo.save()
        return redirect('todo:task_detail', task_id=memo.task.id)  # task画面に戻す

@login_required
def edit_memo(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)

    if request.method == 'POST':
        memo.context = request.POST.get('context')
        memo.save()
        return redirect('todo:task_detail', task_id=memo.task.id)

    # GETで来た場合は task_detail にリダイレクト（直接URL叩かれたとき）
    return redirect('todo:task_detail', task_id=memo.task.id)

@login_required
def delete_memo(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)
    task_id = memo.task.id
    memo.delete()
    return redirect('todo:task_detail', task_id=task_id)

@require_POST
@login_required
def toggle_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    like, created = Like.objects.get_or_create(comment=comment, user=user)
    if not created:
        like.delete()

    return redirect(f"{reverse('todo:task_detail', args=[comment.task.id])}?view=comment")
