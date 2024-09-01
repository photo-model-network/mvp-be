release: python manage.py collectstatic --noinput
web: ddtrace-run uvicorn config.asgi:application --host 0.0.0.0 --port ${PORT:-8000}