from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from todo.models import Task
from accounts.models import Profile

@login_required
def index(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    # 予定日を保存（POST処理）
    if request.method == "POST":
        planned_date = request.POST.get('planned_move_date')
        if planned_date:
            profile.planned_move_date = planned_date
            profile.save()
            messages.success(request, "予定日を保存しました！")
            return redirect('home')  # 保存後リロード

    # タスク情報
    tasks = Task.objects.filter(user=user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_done=True).count()
    percent = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0

    # 残り日数
    today = timezone.now().date()
    remaining_days = (profile.planned_move_date - today).days if profile.planned_move_date else None

    # お知らせタスク
    upcoming_tasks = tasks.filter(
        due_date__isnull=False, 
        due_date__gte=today, 
        due_date__lte=today + timedelta(days=2)
    ).order_by('due_date')
    
    today_tasks = tasks.filter(due_date=today)

    context = {
        'planned_move_date': profile.planned_move_date,
        'remaining_days': remaining_days,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'percent': percent,
        'upcoming_tasks': upcoming_tasks,
        'today_tasks': today_tasks,
    }
    return render(request, 'home/index.html', context)
