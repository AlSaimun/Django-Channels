"""
ASGI config for Simple_Chat_APP project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import app.rounting


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Simple_Chat_APP.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':URLRouter(
        app.rounting.websocket_urlpatterns
    )
})
