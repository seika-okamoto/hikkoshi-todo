from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta, datetime, date
from todo.models import Task
from accounts.models import Profile
from django.db.models import F
from django.db.models import Q


@login_required
def index(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    # 予定日を保存（POST処理）
    if request.method == "POST":
        planned_date = request.POST.get('planned_move_date')
        try:
            if planned_date:
                profile.planned_move_date = datetime.strptime(planned_date, "%Y-%m-%d").date()
                profile.save()

                # 🔥 tasks の定義（POST内にも必要）
                tasks = Task.objects.filter(user=user)

                # タスクの due_date を再計算
                for task in tasks:
                    if task.category and task.category.days_before is not None:
                        task.due_date = profile.planned_move_date - timedelta(days=task.category.days_before)
                        task.save()

                messages.success(request, "引っ越し予定日を保存しました！")
            return redirect('home:index')
        except Exception as e:
            messages.error(request, f"保存中にエラーが発生しました: {str(e)}")
            return redirect('home:index')

    # 👇 POST後のGET処理や初回アクセス用ここから
    profile.refresh_from_db()  # ←念のためリロード！

    tasks = Task.objects.filter(user=user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_done=True).count()
    today = timezone.now().date()

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

    notification_tasks = notifications[:3]
    notification_all_count = len(notifications)
    today_tasks = tasks.filter(due_date=today)

    # 日数・進捗率計算など
    remaining_days = None
    percent = 0
    is_past_due = False
    if profile.planned_move_date:
        delta = (profile.planned_move_date - date.today()).days
        remaining_days = delta
        is_past_due = delta < 0

        percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
    
    context = {
        'planned_move_date': profile.planned_move_date.strftime('%Y-%m-%d') if profile.planned_move_date else '',
        'remaining_days': remaining_days,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'percent': percent,
        'today_tasks': today_tasks,
        'notifications': notifications,
        'notification_tasks': notification_tasks,
        'notification_all_count': notification_all_count,
        'today': today,
        'is_past_due': is_past_due,
        'hide_header': True,
    }

    return render(request, 'home/index.html', context)


def portfolio_view(request):
    return render(request, 'portfolio/portfolio.html', {
        'hide_header': True
    })

def custom_404_view(request, exception):
    return render(request, '404.html', {'hide_header': True}, status=404)

def custom_500_view(request):
    return render(request, '500.html', {'hide_header': True}, status=500)

def custom_403_view(request, exception):
    return render(request, '403.html', {'hide_header': True}, status=403)

def custom_400_view(request, exception):
    return render(request, '400.html', {'hide_header': True}, status=400)