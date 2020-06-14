
def on_connect(client, userdata, flags, rc):
    print("[MQTT] Connected with result code "+str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("[MQTT] Unexpected disconnection.")

def on_log(client, userdata, level, buf):
    print("[MQTT] {}".format(buf))