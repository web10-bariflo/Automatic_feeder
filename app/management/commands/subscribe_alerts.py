import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from app.models import Alert_message

BROKER = "mqttbroker.bc-pl.com"
PORT = 1883
USERNAME = "mqttuser"
PASSWORD = "Bfl@2025"

DEVICE_ID = "BFL_FdtryA001"
SYSTEM_ALERT_TOPIC = f"auto_feeder/{DEVICE_ID}/system/alert"

class Command(BaseCommand):
    help = 'Subscribe to system alert topic and save messages to Alert_message table'

    def handle(self, *args, **options):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS("✅ Connected to MQTT broker"))
                client.subscribe(SYSTEM_ALERT_TOPIC)
                self.stdout.write(self.style.SUCCESS(f"🔔 Subscribed to topic: {SYSTEM_ALERT_TOPIC}"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Connection failed with code {rc}"))

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode()
                self.stdout.write(f"📩 Message: {payload}")
                Alert_message.objects.create(alert=payload)
                self.stdout.write(self.style.SUCCESS("✅ Message saved to Alert_message table"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error saving message: {e}"))

        def on_disconnect(client, userdata, rc):
            self.stdout.write(f"⚠️ Disconnected with code {rc}")
            if rc != 0:
                self.stdout.write("🔄 Attempting to reconnect...")
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
