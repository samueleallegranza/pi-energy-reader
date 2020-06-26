import json
import paho.mqtt.client as mqtt

class Connection():

    mqtt_client = None

    def __init__(self, configFile):
        with open(configFile) as json_file:
            self.config = json.load(json_file)

        self.mqtt_client = mqtt.Client(self.config["name"])
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_log = self.on_log

    def open(self):
        self.mqtt_client.connect(
            host = self.config['address'], 
            port = self.config['port'], 
            keepalive = self.config['keepalive']
        )
        self.mqtt_client.loop_start()

    def publish(self, subtopic, payload, qos=1):
        self.mqtt_client.publish(
            topic=self.config['topic']+'/'+subtopic,
            payload=json.dumps(payload),
            qos=qos
        )

    def on_connect(self, client, userdata, flags, rc):
        print("[MQTT] Connected with result code "+str(rc))

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("[MQTT] Unexpected disconnection.")

    def on_log(self, client, userdata, level, buf):
        print("[MQTT] {}".format(buf))