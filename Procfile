release: python manage.py collectstatic --noinput
web: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uvicorn config.asgi:application --host 0.0.0.0 --port ${PORT:-8000}