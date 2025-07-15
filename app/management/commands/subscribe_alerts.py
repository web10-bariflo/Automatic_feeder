import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from app.models import Alert_message_auto, Alert_message_manual

BROKER = "mqttbroker.bc-pl.com"
PORT = 1883
USERNAME = "mqttuser"
PASSWORD = "Bfl@2025"

DEVICE_ID = "BFL_FdtryA001"
AUTO_STATUS_TOPIC = f"auto_feeder/{DEVICE_ID}/auto/status"
MANUAL_STATUS_TOPIC = f"auto_feeder/{DEVICE_ID}/manual/status"

TOPICS = [
    (AUTO_STATUS_TOPIC, 0),
    (MANUAL_STATUS_TOPIC, 0),
]

class Command(BaseCommand):
    help = 'Subscribe to auto/manual status topics and save messages'

    def handle(self, *args, **options):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS("✅ Connected to MQTT broker"))
                for topic, qos in TOPICS:
                    client.subscribe((topic, qos))
                    self.stdout.write(self.style.SUCCESS(f"🔔 Subscribed to topic: {topic}"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Connection failed with code {rc}"))

        def on_message(client, userdata, msg):
            try:
                topic = msg.topic
                payload = msg.payload.decode()
                self.stdout.write(f"📩 Message from {topic}: {payload}")

                if topic == AUTO_STATUS_TOPIC:
                    Alert_message_auto.objects.create(alert=payload)
                    self.stdout.write(self.style.SUCCESS("✅ Auto status message saved"))

                elif topic == MANUAL_STATUS_TOPIC:
                    Alert_message_manual.objects.create(alert=payload)
                    self.stdout.write(self.style.SUCCESS("✅ Manual status message saved"))

                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Unknown topic: {topic}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error processing message: {e}"))

        def on_disconnect(client, userdata, rc):
            self.stdout.write(f"⚠️ Disconnected (code {rc})")
            if rc != 0:
                self.stdout.write("🔄 Reconnecting...")
                try:
                    client.reconnect()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Reconnection failed: {e}"))

        client = mqtt.Client()
        client.username_pw_set(USERNAME, PASSWORD)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        try:
            client.connect(BROKER, PORT, 60)
            client.loop_forever()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ MQTT connection error: {e}"))
