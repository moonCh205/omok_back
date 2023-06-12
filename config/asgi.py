import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from storage.middlewares import TokenAuthMiddleWare
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")	# mysite 는 django 프로젝트 이름
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

import chat.routing
import game.routing
router = chat.routing.websocket_urlpatterns+game.routing.websocket_urlpatterns# chat 은 routing.py 가 들어있는 앱 이름
                    
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": TokenAuthMiddleWare(
        AllowedHostsOriginValidator(
            URLRouter(
                router
            )
        )
    ),
})