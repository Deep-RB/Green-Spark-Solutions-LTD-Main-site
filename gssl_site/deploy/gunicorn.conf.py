"""
gunicorn settings for the GSSL website.

    gunicorn config.wsgi:application -c deploy/gunicorn.conf.py

Every value can be overridden from the environment (GUNICORN_*), so the
systemd unit or the host panel can tune it without editing this file.
"""

import multiprocessing
import os

# Listen on localhost only: nginx (or the host's proxy) faces the internet.
bind = os.environ.get("GUNICORN_BIND", "127.0.0.1:8000")

# The site is light; a few workers are plenty. Each worker keeps its own
# contact-form throttle counters.
workers = int(os.environ.get("GUNICORN_WORKERS", min(multiprocessing.cpu_count() * 2 + 1, 5)))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 30))
graceful_timeout = 30
keepalive = 5

# Recycle workers now and then so memory never creeps.
max_requests = 1000
max_requests_jitter = 100

# Logs to stdout/stderr; systemd's journal (or the host panel) keeps them.
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

# Trust X-Forwarded-* only from the local proxy.
forwarded_allow_ips = os.environ.get("GUNICORN_FORWARDED_ALLOW_IPS", "127.0.0.1")
