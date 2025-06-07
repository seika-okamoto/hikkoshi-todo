from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta, datetime
from todo.models import Task
from accounts.models import Profile
from django.db.models import F
from django.db.models import Q


@login_required
def index(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    # タスク情報
    tasks = Task.objects.filter(user=user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_done=True).count()
    percent = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0

    # 予定日を保存（POST処理）
    if request.method == "POST":
        planned_date = request.POST.get('planned_move_date')
        if planned_date:
            profile.planned_move_date = datetime.strptime(planned_date, "%Y-%m-%d").date()
            profile.save()
            messages.success(request, "予定日を保存しました！")

            # 🔥 ここでタスクのdue_dateを再計算
            for task in tasks:
                if task.category and task.category.days_before is not None:
                    task.due_date = profile.planned_move_date - timedelta(days=task.category.days_before)
                    task.save()

            return redirect('home:index')



    # 残り日数
    today = timezone.now().date()
    remaining_days = (profile.planned_move_date - today).days if profile.planned_move_date else None

    # お知らせタスク（カテゴリdays_beforeベース）
    notifications = []

    for task in tasks.filter(due_date__isnull=False, is_done=False).order_by('due_date', 'id'):
        days_left = (task.due_date - today).days

        if days_left < 0:
            notifications.append({'task': task, 'status': '期限切れ'})
        elif days_left == 0:
            notifications.append({'task': task, 'status': '今日が期限'})
        elif days_left == 1:
            notifications.append({'task': task, 'status': 'あと1日'})
        elif days_left == 2:
            notifications.append({'task': task, 'status': 'あと2日'})
        elif days_left <= 7:
            notifications.append({'task': task, 'status': f'あと{days_left}日'})

    # 最大3件まで
    notification_tasks = notifications[:3]

    # 3件以上ならフラグを立てる
    notification_all_count = len(notifications)


    today_tasks = tasks.filter(due_date=today)

    context = {
        'planned_move_date': profile.planned_move_date,
        'remaining_days': remaining_days,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'percent': percent,
        'today_tasks': today_tasks,
        'notifications': notifications,
        'notification_tasks': notification_tasks,
        'notification_all_count': notification_all_count,
        'today': today,  # 今日の日付をテンプレートでも使えるように渡す
    }
    context['hide_header'] = True
    return render(request, 'home/index.html', context)

