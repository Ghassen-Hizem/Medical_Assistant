from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from bioBertApi.consumers import PracticeConsumer
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BackendMedical.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
            path('api', PracticeConsumer.as_asgi())
        ])
})