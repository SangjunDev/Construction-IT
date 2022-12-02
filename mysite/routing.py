#from channels.auth import AuthMiddlewareStack
#from channels.routing import ProtocolTypeRouter, URLRouter
#import mqttchannel.routing

#application = ProtocolTypeRouter({
#    'websocket': AuthMiddlewareStack(
#        URLRouter(
#            mqttchannel.routing.websocket_urlpatterns
#        )
#    ),
#})

import os
import django
from channels.routing import ProtocolTypeRouter
from mqttchannel.consumers import MyMqttConsumer
from django.core.asgi import get_asgi_application

from chanmqttproxy import MqttConsumer
from channels.routing import ChannelNameRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

django.setup()

application = ProtocolTypeRouter({
        "channel": ChannelNameRouter({
			"mqtt": MqttConsumer.as_asgi()
		}),
    })