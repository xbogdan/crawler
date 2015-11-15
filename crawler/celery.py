from celery import Celery

app = Celery('hello', broker='redis://localhost:6379/0')