from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # ユーザー名
        password = request.POST.get('password')  # パスワード
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('todo:index')  # 成功したらtodoアプリのトップへ
        else:
            messages.error(request, 'ユーザー名またはパスワードが間違っています')
    
    return render(request, 'accounts/login.html')

