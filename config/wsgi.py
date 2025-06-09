"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
import os
import sys

# manage.py があるディレクトリを追加（正しいパス）
path = '/home/seika1224/hikkoshi-todo'
if path not in sys.path:
    sys.path.append(path)

# DJANGO_SETTINGS_MODULE を明示（絶対にこれにする！）
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# ログを仕込んで読み込み確認
print("✅ WSGIファイルが読み込まれた！")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
