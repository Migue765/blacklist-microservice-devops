release: python scripts/notify_newrelic_deployment.py
web: gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 60 --access-logfile - --error-logfile - --log-level info application:application