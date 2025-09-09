from app import init
import multiprocessing

wsgi_app = "app:app"
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2
preload_app = True
worker_class = "gthread"
def on_starting(server):
    init()
