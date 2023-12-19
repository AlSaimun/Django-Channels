from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/sc/', consumers.DemoSyncConsumer.as_asgi()),
    path('ws/asc/', consumers.DemoAsyncConsumer.as_asgi()),
]