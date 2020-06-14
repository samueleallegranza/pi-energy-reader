from datetime import datetime
import time

from U_modbus import interface
from AutoPriorityQueue import queue
from FixedScheduler import scheduler

import json
import paho.mqtt.client as mqtt

import mqtt_setup

# Message displayed when no config broker file is detected
def messageRequiredConfig():
    print(
    """
    Configuration file 'config/meters/config_BROKER.json' NOT FOUND
    Please, create it and put the informations like this:
        {
            address:    ip of the broker
            port:       port of the broker
            topic:      topic to publish
        }
    """
    )

def modbus_execute(meter, field):
    return meter.execute(field)

def readLive():
    global enel_meter, solar_meter
    global ap_queue
    global mqttClient

    currTime = (int(time.time())) * 1000 #milliseconds
    try:
        enel_task = ap_queue.add(1, modbus_execute, (enel_meter, "ACTIVE_POWER"))
        solar_task = ap_queue.add(1, modbus_execute, (solar_meter, "ACTIVE_POWER"))
        enel_result = enel_task.getResult()
        solar_result = solar_task.getResult()

        mqttPayload = {"type": "liveData", "time": currTime, "liveEnel": enel_result, "liveSolar": solar_result}
        print("{} - PAYLOAD: {}".format(datetime.now(), mqttPayload))
        mqttClient.publish("liveData", json.dumps(mqttPayload), qos=1)
    except Exception as e:
        print("ERROR occurred (probably) while reading from meters")
        print("Details: " + e)


def readSummary():
    global enel_meter, solar_meter
    global ap_queue
    global mqttClient

    currTime = (int(time.time())) * 1000 #milliseconds
    try:
        enelIn_task = ap_queue.add(2, modbus_execute, (enel_meter, "IMPORT_ACTIVE_ENERGY"))
        enelOut_task = ap_queue.add(2, modbus_execute, (enel_meter, "EXPORT_ACTIVE_ENERGY"))
        solarIn_task = ap_queue.add(2, modbus_execute, (solar_meter, "TOTAL_ACTIVE_ENERGY"))
        enelIn_result = enelIn_task.getResult()
        enelOut_result = enelOut_task.getResult()
        solarIn_result = solarIn_task.getResult()

        mqttPayload = {"type": "summaryData", "time": currTime, "enelIn": enelIn_result, "enelOut": enelOut_result, "solarIn": solarIn_result}
        print("{} - PAYLOAD: {}".format(datetime.now(), mqttPayload))
        mqttClient.publish("liveData", json.dumps(mqttPayload), qos=1)
    except Exception:
        print("ERROR occurred (probably) while reading from meters")



# MAIN: Setup of the project
if __name__ == "__main__":

    # Energy meters
    enel_meter = interface.Device("./config/meters/config_UEM40.json")
    solar_meter = interface.Device("./config/meters/config_SDM120.json")
    enel_meter.open()
    solar_meter.open()

    # MQTT Broker
    try:
        with open("./config/mqtt/config_BROKER.json", 'r') as config_txt:
            config = json.load(config_txt)
            mqttClient = mqtt.Client("Rpi-1")
            mqttClient.on_connect = mqtt_setup.on_connect
            mqttClient.on_disconnect = mqtt_setup.on_disconnect
            mqttClient.on_log = mqtt_setup.on_log
            mqttClient.connect(config['address'], config['port'], keepalive=60)
            mqttClient.loop_start()
    except FileNotFoundError as err:
        messageRequiredConfig()
        sys.exit(1)

    # Automatic Queue
    ap_queue = queue.Queue()

    # Scheduler
    sched = scheduler.Scheduler(0.01)
    sched.addTask(1, readLive)
    sched.addTask(60, readSummary)
    sched.start()
