from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from todo.models import Task  # ← Taskモデルをインポート

@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_done=True).count()
    percent = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
    
    
    return render(request, 'home/index.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'percent': percent,
    })

