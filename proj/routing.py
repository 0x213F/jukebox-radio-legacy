from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.security.websocket import OriginValidator

from proj.apps.consumers import Consumer


application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter([url("", Consumer)]))
        )
    }
)
