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

    # タスク情報
    tasks = Task.objects.filter(user=user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_done=True).count()
    
    # 残り日数
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

    # 最大3件まで
    notification_tasks = notifications[:3]

    # 3件以上ならフラグを立てる
    notification_all_count = len(notifications)


    today_tasks = tasks.filter(due_date=today)

# GET: context定義（←ここで表示用データ整える！）
    remaining_days = None
    percent = 0
    is_past_due = False
    
    if profile.planned_move_date:
        delta = (profile.planned_move_date - date.today()).days
        remaining_days = delta
        percent = max(0, 100 - delta)  # 仮に進捗表示させるなら
        is_past_due = delta < 0

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
        'is_past_due': is_past_due,
        'hide_header': True,
    }
    
       # 予定日を保存（POST処理）
    if request.method == "POST":
        planned_date = request.POST.get('planned_move_date')
        try:
            if planned_date:
                profile.planned_move_date = datetime.strptime(planned_date, "%Y-%m-%d").date()
                profile.save()
                
                # 🔥 ここでタスクのdue_dateを再計算
                for task in tasks:
                    if task.category and task.category.days_before is not None:
                        task.due_date = profile.planned_move_date - timedelta(days=task.category.days_before)
                        task.save()
                messages.success(request, "引っ越し予定日を保存しました！")
            return redirect('home:index')
        except Exception as e:
            messages.error(request, f"保存中にエラーが発生しました: {str(e)}")
                # ⚠️ リダイレクトせずにそのまま進む（contextを定義してから render する）
            return redirect('home:index')

       
    return render(request, 'home/index.html', context)

def portfolio_view(request):
    return render(request, 'portfolio/portfolio.html',{
                  'hide_header': True
                  })