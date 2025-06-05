from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .forms import SignUpForm
from todo.models import Task ,Category
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.urls import reverse
from .models import EmailChangeToken
from django.shortcuts import get_object_or_404, redirect
from todo.models import Comment 
from .forms import CommentForm  



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ← 登録と同時にログインさせる！

            # Profile作成
            Profile.objects.create(user=user)
            print(f"✅ プロフィール作成: {user.email}")
            
            tasks_data = {
                "引っ越し1か月前までにやること": [
                    "引っ越し日を決定する",
                    "引っ越し業者探し（見積もりを取る）",
                    "現在の住まいの管理会社に引っ越し・退去の連絡",
                    "インターネットの申し込み手続き",
                    "インターネットの解約手続き",
                    "新居の採寸",
                    "勤務先への住所変更の届出",
                    "新居物件契約と初期費用の支払い",
                    "立ち合い日時の確定（賃貸の方のみ）",
                    "NHKやサブすくの住所変更（契約者の方のみ）",
                    "不要品・粗大ごみの処分方法の検討",
                    "学校や園に転校・転園の連絡",
                    "保育園・幼稚園の転園申請",
                ],
                "引っ越し3週間前までにやること": [
                    "必要な梱包材を準備",
                    "粗大ごみの収集申し込み",
                    "不用品の仕分け",
                    "新居の家具・家電のレイアウト検討",
                    "新規で購入が必要なものの手配",
                ],
                "引っ越し2週間前までにやること": [
                    "使用頻度の低いものから梱包",
                    "オフシーズンの衣類などの梱包",
                    "必要な衣類・本などの処分・売却",
                    "定期配達サービスの契約変更・解約（利用者のみ）",
                ],
                "引っ越し1週間前までにやること": [
                    "粗大ごみの処分",
                    "使用頻度の高いものを梱包",
                    "郵便局への連絡（転居・転送）",
                    "転出届を出す",
                    "児童手当や乳幼児医療費受給資格者証の手続き",
                    "電気会社への停止・解約連絡（現住所）",
                    "ガス会社への停止・解約連絡（現住所）",
                    "水道局への停止・解約連絡（現住所）",
                    "引っ越し挨拶の手土産の準備",
                    "ゴミ出し",
                ],
                "引っ越し前日までにやること": [
                    "洗濯機の水抜き",
                    "冷蔵庫の中を空に、電源を切る",
                    "引っ越し当日、すぐ使うものをまとめる",
                    "旧居のお掃除",
                    "引っ越し当日の新居までの移動方法を確認",
                    "引っ越し挨拶（旧居）",
                ],
                "引っ越し当日にやること": [
                    "引っ越し料金の支払い準備",
                    "電力停止の立ち合い（現住所）",
                    "ガス停止の立ち合い（現住所）",
                    "水道の停止立ち合い（現住所）",
                    "新居の初期状態の記録を残す（傷・汚れなど撮影）",
                    "ガスの開栓の立ち合い（新居）",
                    "水道局への開栓・開始連絡（新居）",
                    "荷物の搬出",
                    "搬出後の忘れ物がないかチェック",
                    "搬出後の掃除、ゴミなどの処分",
                    "退室前にブレーカーを下げる",
                    "新居のブレーカーを上げる",
                    "家具など大きいものから搬入",
                    "夜になる前にカーテン・照明を設置",
                ],
                "引っ越し後1週間以内にやること": [
                    "旧居の鍵返却と退去の立ち会い",
                    "運転免許証の住所変更",
                    "引っ越しの挨拶（新居・近隣）",
                ],
                "引っ越し後の2週間以内にやること": [
                    "転入届を出す",
                    "マイナンバーカードの住所変更",
                    "印鑑登録の住所変更・登録手続き",
                    "児童手当の住所変更・認定請求書の提出",
                    "乳幼児医療費受給資格証の住所変更・申請",
                    "車検証の住所変更手続き",
                    "銀行・保険・証券会社などの住所変更",
                    "クレジットカードの住所変更手続き",
                    "引っ越しのお知らせを友人などに送る",
                ],
            }
            
            print("✅ タスク登録スタート！")
            for category_name, tasks in tasks_data.items():
                category_obj = Category.objects.get(name=category_name)  # ← Categoryオブジェクトを取得！
                if category_obj is None:
                    print(f"⚠️ カテゴリが見つからない: {category_name}")
                    continue
                            
                for title in tasks:
                    Task.objects.create(
                        user=user,
                        title=title,
                        category=category_obj,
                        is_done=False
                    )

            return redirect('todo:index')  # ← 初期登録済みでToDoへ遷移
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

@login_required
def mypage_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/mypage.html', {
        'profile': profile,
        'hide_header': True
        })

@login_required
def edit_username(request):
    profile = request.user.profile
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if new_username:
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'ニックネームを更新しました')
        return redirect('accounts:mypage')
    else:
        return redirect('accounts:mypage')
    
@login_required
def edit_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        password = request.POST.get('password')
        user = authenticate(request, email=request.user.email, password=password)
        print("📌 パスワード認証結果:", user)

        if user is not None:
            # ✅ ここでトークンを作って保存！
            email_token = EmailChangeToken.objects.create(
                user=request.user,
                new_email=new_email,
            )

            # ✅ 確認リンク生成
            confirm_url = request.build_absolute_uri(
                reverse('accounts:confirm_email_change', kwargs={'token': email_token.token})
            )

            # ✅ メール送信
            send_mail(
                'メールアドレス変更の確認',
                f'以下のリンクをクリックしてメールアドレスを変更してください：\n{confirm_url}',
                'no-reply@example.com',
                [new_email],
                fail_silently=False,
            )
            print("メール送信完了")

            return redirect(f"{reverse('accounts:email_change_sent')}?email={new_email}")
        else:
            # パスワードが間違っている場合など
            messages.error(request, 'パスワードが正しくありません。')

    # ✅ GETリクエスト or エラー時にフォーム表示
    return render(request, 'accounts/edit_email.html')


@login_required
def email_change_sent(request):
    new_email = request.GET.get('email')
    return render(request, 'accounts/email_change_sent.html', {'new_email': new_email, 'hide_header': True})

@login_required
def confirm_email_change(request, token):
    token_obj = get_object_or_404(EmailChangeToken, token=token)

    if token_obj.is_expired():
        messages.error(request, '確認リンクの有効期限が切れています。')
        return redirect('accounts:mypage')

    user = token_obj.user
    user.email = token_obj.new_email
    user.save()

    # トークン削除（もしくは使用済みにしてもOK）
    token_obj.delete()

    messages.success(request, 'メールアドレスを変更しました！')
    return redirect('accounts:mypage')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # ログイン状態維持
            messages.success(request, 'パスワードを変更しました')
            return redirect('accounts:mypage')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def comment_history(request):
    user_comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/comment_history.html', {'comments': user_comments})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        if 'save' in request.POST:
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('accounts:comment_history')
        elif 'delete' in request.POST:
            comment.delete()
            return redirect('accounts:comment_history')
    else:
        form = CommentForm(instance=comment)
        print(form.errors)

    return render(request, 'accounts/edit_comment.html', {'form': form})

@login_required
def about_app(request):
    return render(request, 'accounts/about_app.html')