from django.conf.urls import url
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.security.websocket import OriginValidator

from proj.apps.music.consumers import ShowingConsumer
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url('', ShowingConsumer)
                ]
            )
        )
    )
})
