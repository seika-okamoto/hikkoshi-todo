from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .forms import SignUpForm

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

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # ログアウト後にログイン画面に戻す

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # 登録後ログイン画面へ
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})