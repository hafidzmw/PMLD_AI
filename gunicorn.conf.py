import os
import multiprocessing
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("GUNICORN_HOST", "0.0.0.0")
port = os.getenv("GUNICORN_PORT", "5000")
bind = f"{host}:{port}"

workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
timeout = int(os.getenv("GUNICORN_TIMEOUT", 30))

accesslog = os.getenv("GUNICORN_ACCESS_LOG", "/app/logs/access.log")
errorlog = os.getenv("GUNICORN_ERROR_LOG", "/app/logs/error.log")
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

preload_app = os.getenv("GUNICORN_PRELOAD", "true").lower() in ["true", "1", "yes"]