
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import app.rounting
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SimpleProject.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        app.rounting.websocket_urlpatterns
    )
})
