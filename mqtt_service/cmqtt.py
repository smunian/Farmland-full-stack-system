# mqtt 客户端
import datetime

import paho.mqtt.client as mqtt
import json
from django.core.cache import cache

MQTT_USERNAME = "123"
MQTT_USERNAME2 = "1234"
MQTT_PASSWORD = "1222"
MQTT_PASSWORD2 = "1222"

MQTT_BROKER = "localhost"
MQTT_PORT = 1883


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client2 = mqtt.Client()
        self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.client2.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.client.on_message = self.save_data
        self.client2.on_message = self.is_online
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client2.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.subscribe("agriculture")
        self.client2.subscribe("$SYS/brokers/+/clients/#")
        self.client.loop_start()
        self.client2.loop_start()

    def save_data(self, client, userdata, message):
        from api.models import SensorMonitor_info
        try:
            getdata = message.payload.decode("utf-8")
            data = json.loads(getdata)
            if float(data['device_data']['soi_humidity']) > 100:
                soi_humidity = 100,
            else:
                soi_humidity = data['device_data']['soi_humidity']
            s = SensorMonitor_info(
                device_info_id=data['device_id'],
                temperature=data['device_data']['temperature'],
                humidity=data['device_data']['humidity'],
                soi_humidity=soi_humidity,
                co2=data['device_data']['co2'],
                luminance=data['device_data']['luminance'],
            )
            s.save()
        except Exception as e:
            print(e)
            # print("未授权设备" + data["device_id"])

    def is_online(self, client, userdata, message):
        from api.models import device_history, device
        online_data = message.payload.decode("utf-8")
        data = json.loads(online_data)
        clientid = data["clientid"]
        try:
            if "disconnected_at" in data:
                disconnected_at_millis = data["disconnected_at"]
                connected_at_millis = data["connected_at"]

                # 将毫秒级时间戳转换为秒级时间戳
                disconnected_at_seconds = disconnected_at_millis / 1000
                connected_at_seconds = connected_at_millis / 1000
                # 使用datetime.fromtimestamp将秒级时间戳转换为datetime对象

                # 注意：这里假设时间戳是基于UTC的，如果你的时间戳是基于其他时区的，需要相应地处理
                disconnected_at_datetime = datetime.datetime.fromtimestamp(disconnected_at_seconds)
                connected_at_datetime = datetime.datetime.fromtimestamp(connected_at_seconds)

                duration_seconds = (disconnected_at_datetime - connected_at_datetime).total_seconds()
                duration_minutes = int(duration_seconds // 60)

                disconnected_at_datetime = disconnected_at_datetime.strftime("%Y-%m-%d %H:%M:%S")
                connected_at_datetime = connected_at_datetime.strftime("%Y-%m-%d %H:%M:%S")
                device_history_s = device_history(device_id=data["clientid"], device_online=connected_at_datetime,
                                                  device_offline=disconnected_at_datetime, duration=duration_minutes)
                device_history_s.save()
                cache.set(clientid, 0)
            else:
                if cache.get(clientid) == 0:
                    connected_at_millis = data["connected_at"]
                    connected_at_seconds = connected_at_millis / 1000
                    connected_at_datetime = datetime.datetime.fromtimestamp(connected_at_seconds)
                    connected_at_datetime = connected_at_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    device.objects.filter(device_id=data["clientid"]).update(last_online=connected_at_datetime)
                cache.set(clientid, 1)
        except Exception as e:
            print(e)
        print(cache.get(clientid))

    def is_open(self, a, device):
        if device == 'light':
            if a:
                payload = {
                    "clientid": "lzdz",
                    "equipment": "light",
                    "control": 1
                }
            else:
                payload = {
                    "clientid": "lzdz",
                    "equipment": "light",
                    "control": 0
                }
        else:
            if a:
                payload = {
                    "clientid": "lzdz",
                    "equipment": "water",
                    "control": 0
                }
            else:
                payload = {
                    "clientid": "lzdz",
                    "equipment": "water",
                    "control": 1
                }
            # 假设 self.client 是一个有效的 MQTT 客户端实例，并且它有一个 publish 方法
        self.client.publish("cagriculture", json.dumps(payload))
