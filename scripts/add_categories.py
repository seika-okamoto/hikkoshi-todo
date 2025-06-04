import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from todo.models import Category

category_names = [
    "引っ越し1か月前までにやること",
    "引っ越し3週間前までにやること",
    "引っ越し2週間前までにやること",
    "引っ越し1週間前までにやること",
    "引っ越し前日までにやること",
    "引っ越し当日にやること",
    "引っ越し後1週間以内にやること",
    "引っ越し後の2週間以内にやること",
]

for name in category_names:
    category, created = Category.objects.get_or_create(name=name)
    if created:
        print(f"✅ カテゴリ作成: {name}")
    else:
        print(f"🔁 すでに存在: {name}")
