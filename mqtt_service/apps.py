from django.apps import AppConfig
from mqtt_service.cmqtt import *

mqtt_clinet = MQTTClient()


class MqttServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt_service'

