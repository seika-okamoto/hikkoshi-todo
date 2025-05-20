from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task



@login_required  # ← ログインしてる人だけアクセスできる
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'todo/index.html', {'tasks': tasks})