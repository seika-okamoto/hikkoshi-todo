from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ← 登録と同時にログインさせる！
            return redirect('todo:index')  # ← ログイン済みでtodoへ遷移
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # ← email に書き換え
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)  # ← ここもemailを使う

        if user is not None:
            login(request, user)
            return redirect('todo:index')  # 成功したらtodoアプリのトップへ
        else:
            messages.error(request, 'メールアドレスまたはパスワードが間違っています')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # ログアウト後にログイン画面に戻す
