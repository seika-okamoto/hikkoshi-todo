from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from todo.models import Task  # ← Taskモデルをインポート
from accounts.models import Profile
from django.utils import timezone
from datetime import date
from django.contrib import messages


@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_done=True).count()
    percent = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
    profile, created = Profile.objects.get_or_create(user=request.user)
    remaining_days = None
    
    if profile.planned_move_date:
        today = date.today()
        remaining_days = (profile.planned_move_date - today).days
    
    if request.method == "POST":
        planned_date = request.POST.get('planned_move_date')
        profile = Profile.objects.get(user=request.user)
        profile.planned_move_date = planned_date
        profile.save()
        messages.success(request, "予定日を保存しました！")

    
    return render(request, 'home/index.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'percent': percent,
        'profile': profile, 
        'remaining_days': remaining_days
    })
    
def set_move_date(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        move_date = request.POST.get('planned_move_date')
        if move_date:
            profile.planned_move_date = move_date
            profile.save()
            print(f"✅ 引っ越し予定日を更新: {move_date}")
            return redirect('home')  # ホーム画面に戻す

    return render(request, 'home/set_move_date.html', {'profile': profile})

