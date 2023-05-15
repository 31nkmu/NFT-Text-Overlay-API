from celery import Celery

from src import config

app = Celery('config', broker='redis://localhost:6379')

app.config_from_object('src:config')  # берет настройки селепи из src.config директории
app.autodiscover_tasks(lambda: config.APPS)  # ищет задачи во всех модулях tasks
