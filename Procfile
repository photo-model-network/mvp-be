release: python manage.py collectstatic --noinput
web: uvicorn config.asgi:application --host 0.0.0.0 --port ${PORT:-8000}