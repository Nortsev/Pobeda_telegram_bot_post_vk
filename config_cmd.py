from os import environ as env
import multiprocessing

PORT = int(env.get("PORT", 1313))
DEBUG = int(env.get("DEBUG", 1))
ENVIRONMENT = env.get('ENVIRONMENT', 'local')

# Gunicorn config
bind = f":{PORT}"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()