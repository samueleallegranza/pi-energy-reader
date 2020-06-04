from datetime import datetime
import time

from U_modbus import interface
from FixedScheduler import scheduler
from AutoPriorityQueue import queue


def readLive():
    global enel_meter, solar_meter
    # global broker_topic
    # broker_qos = 1

    currTime = (int(time.time())) * 1000 #milliseconds
    try:
        liveEnel = enel_meter.execute("ACTIVE_POWER")
        liveSolar = solar_meter.execute("ACTIVE_POWER")
        mqttPayload = {"time": currTime, "liveEnel": liveEnel, "liveSolar": liveSolar}
        print("{} - PAYLOAD: {}".format(datetime.now(), mqttPayload))
        # mqttPub.publish(strC(broker_topic), strC(json.dumps(mqttPayload)), intC(broker_qos))
    except Exception as e:
        print("ERROR occurred (probably) while reading from meters")
        print("Details: " + e)

def task_readLive():
    global q
    q.add(1, readLive, ())


def readSummary():
    global enel_meter, solar_meter
    # global broker_topic
    # broker_qos = 1

    currTime = (int(time.time())) * 1000 #milliseconds
    try:
        liveEnel = enel_meter.execute("ACTIVE_POWER")
        liveSolar = solar_meter.execute("ACTIVE_POWER")
        mqttPayload = {"time": currTime, "liveEnel": liveEnel, "liveSolar": liveSolar}
        print("{} - PAYLOAD: {}".format(datetime.now(), mqttPayload))
        # mqttPub.publish(strC(broker_topic), strC(json.dumps(mqttPayload)), intC(broker_qos))
    except Exception as e:
        print("ERROR occurred (probably) while reading from meters")
        print("Details: " + e)



if __name__ == "__main__":

    # Energy meters
    enel_meter = interface.Device("./meters/config_UEM40.json")
    solar_meter = interface.Device("./meters/config_SDM120.json")
    enel_meter.open()
    solar_meter.open()

    # Automatic Queue
    q = queue.Queue()

    # Scheduler
    sched = scheduler.Scheduler(0.01)
    sched.addTask(1, task_readLive)
    sched.start()


    # while True:
    #     q.add(1, fun1, ('fn1 start', 'fn1 stop'))
    #     q.add(2, fun1, ('fn2 start', 'fn2 stop'))
    #     q.add(1, fun1, ('fn1 start', 'fn1 stop'))

    #     time.sleep(2.5)


    # sched = scheduler.Scheduler(0.01)

    # sched.addTask(1, instant_values)
    # sched.addTask(5, kwh_values, ('arg11', 22))
    
    # sched.start()



# if __name__ == "__main__":

#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

#     logging.info("Main    : create and start threads")
    
#     sched1 = threading.Thread(target=scheduler, args=('sched1', 1,))
#     sched2 = threading.Thread(target=scheduler, args=('sched2', 10,))

#     sched1.start()
#     sched2.start()
