import json, time

class Task():

    mqtt_client = None
    meters_container = None

    def __init__(self, configFile):
        with open(configFile) as json_file:
            self.config = json.load(json_file)
    
    def link(self, mqtt_client, meters_container, queue):
        self.mqtt_client = mqtt_client
        self.meters_container = meters_container
        self.queue = queue

    def _modbus_exec(self, meter_name, command):
        return self.meters_container[meter_name].execute(command)

    def getTask(self):
        current_time = (int(time.time())) * 1000 #milliseconds
        results = {}
        mqtt_payload = {}
                
        try:
            for action in self.config["actions"]:
                results[action["json_field"]] = (
                    self.queue.add(
                        action["priority"],
                        self._modbus_exec,
                        (action["meter"], action["command"])
                    )
                )

            for action in self.config["actions"]:
                mqtt_payload[action["json_field"]] = results[action["json_field"]].getResult()

            
            mqtt_payload["time"] = current_time
            mqtt_subtopic = self.config["mqtt_subtopic"]

            self.mqtt_client.publish(mqtt_subtopic, mqtt_payload, qos=1)
            print(mqtt_payload)
        
        except Exception as exc:
            print("\tException occurred while executing task!\nDetails: {}".format(exc))
