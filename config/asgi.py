"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from ddtrace.contrib.asgi import TraceMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from django.core.asgi import get_asgi_application
from api.chats.routing import websocket_urlpatterns

django_asgi_application = get_asgi_application()

# TraceMiddleware로 Django ASGI 애플리케이션을 감쌈
traced_django_asgi_application = TraceMiddleware(django_asgi_application)


application = ProtocolTypeRouter(
    {
        "http": traced_django_asgi_application,
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
