import os, sys

from app.parser.parser import Parser
from app.scheduler.queue import APQueue
from app.scheduler.scheduler import FixedScheduler


class EnergyReader():

    meters_parser = None
    tasks_parser = None
    mqtt_parser = None

    meters_container = None
    tasks_container = None
    mqtt_client = None

    queue = APQueue()
    scheduler = None

    def __init__(self, config_path, scheduler_resolution=0.01):
        self.check_configpath(config_path)
        
        self.meters_parser = Parser("meters", config_path)
        self.meters_container = self.meters_parser.parse()
        self.configure_meters()

        self.mqtt_parser = Parser("mqtt", config_path)
        self.mqtt_client = self.mqtt_parser.parse()
        self.configure_mqtt()

        self.tasks_parser = Parser("tasks", config_path)
        self.tasks_container = self.tasks_parser.parse()

        self.scheduler = FixedScheduler(scheduler_resolution)
        self.configure_tasks()

    def check_configpath(self, config_path):
        if os.path.exists(config_path):
            print("Ok - Config path ({}) exists!". format(config_path))
        else:
            print("Error - Config path ({}) doesn't exist!". format(config_path))
            sys.exit(1)

    def configure_meters(self):
        for key in self.meters_container:
            self.meters_container[key].open()

    def configure_mqtt(self):
        self.mqtt_client.open()

    def configure_tasks(self):
        for key in self.tasks_container:
            self.tasks_container[key].link(self.mqtt_client, self.meters_container, self.queue)
            task = self.tasks_container[key].getTask
            self.scheduler.addTask(self.tasks_container[key].config["interval"], task)
        self.scheduler.start()