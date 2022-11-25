from django.apps import AppConfig


class MqttwebsocketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqttWebsocket'

class CoreConfig(AppConfig):
    name = 'untitled.core'
    verbose_name = "Core"

    def ready(self):
        from . import mqttWebsocket as mqtt
        mqtt.client.loop_start()