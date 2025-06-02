from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=128)
    order = models.PositiveIntegerField(default=0)
    days_before = models.IntegerField(default=0) 
    
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

    def __str__(self):
        return self.title

class Memo(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='memos')  # 関連するタスク
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 投稿者
    context = models.TextField()  # メモの内容
    created = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return self.context[:20]  # 内容の先頭20文字を表示


