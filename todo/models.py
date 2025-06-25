from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField(default=0)  
    days_before = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)      # 更新日時


    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    memo = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_template = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)  # コメント閲覧可能か
    original_title = models.CharField(max_length=100, blank=True, null=True)

    # ✅ 元のテンプレートタスク（自分のタスクならここにテンプレートが入る）
    original_template = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clones'
    )

    def __str__(self):
        return self.title

class Memo(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='memos')  # 関連するタスク
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 投稿者
    context = models.TextField()  # メモの内容
    created_at = models.DateTimeField(auto_now_add=True)  # ← 名前修正
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return self.context[:20]  # 内容の先頭20文字を表示

class Comment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    display_name = models.CharField(
        max_length=10,
        choices=[('nickname', 'ニックネームで表示'), ('anonymous', '非公開で表示')],
        default='nickname'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]  # コメント内容の先頭20文字を表示

class Like(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('comment', 'user')  # 同じユーザーが同じコメントに複数いいねできないようにする

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"
