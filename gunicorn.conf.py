from app import init
import multiprocessing

wsgi_app = "app:app"
bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() * 2
preload_app = True
def on_starting(server):
    init()
