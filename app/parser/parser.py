import sys, os, json
# from jsonargparse import ActionJsonSchema

from app.U_modbus import interface as modbus
from app.mqtt import interface as mqtt
from app.tasks import interface as tasks

class Mqtt_model():
    _filepaths = []

    def __init__(self, config_path):
        self.config_path = config_path

    def checkFolder(self):
        for file in os.listdir(self.config_path):
            if file.endswith(".json"):
                self._filepaths.append(os.path.join(self.config_path, file))
            else:
                continue

        return (len(self._filepaths) == 1)

    def checkFiles(self):
        return True

    def generateContainer(self):
        return mqtt.Connection(self._filepaths[0])


class Tasks_model():
    _filepaths = []

    def __init__(self, config_path):
        self.config_path = config_path

    def checkFolder(self):
        for file in os.listdir(self.config_path):
            if file.endswith(".json"):
                self._filepaths.append(os.path.join(self.config_path, file))
            else:
                continue

        return (len(self._filepaths) > 0)

    def checkFiles(self):
        return True

    def generateContainer(self):
        container = {}
        for filepath in self._filepaths:
            with open(filepath) as file:
                name = json.load(file)["name"]
                container[name] = tasks.Task(filepath)

        return container


class Meters_model():
    _filepaths = []

    def __init__(self, config_path):
        self.config_path = config_path

    def checkFolder(self):
        for file in os.listdir(self.config_path):
            if file.endswith(".json"):
                self._filepaths.append(os.path.join(self.config_path, file))
            else:
                continue

        return (len(self._filepaths) > 0)

    def checkFiles(self):
        return True

    def generateContainer(self):
        container = {}
        for filepath in self._filepaths:
            with open(filepath) as file:
                name = json.load(file)["tag"]
                container[name] = modbus.Device(filepath)

        return container




config_models = {
    "mqtt": Mqtt_model,
    "tasks": Tasks_model,
    "meters": Meters_model
}

class Parser():

    def __init__(self, model, config_path):
        self.model = model
        self.parser = config_models[model](config_path+'/'+model)

    def parse(self):
        if self.parser.checkFolder():
            if self.parser.checkFiles():
                return self.parser.generateContainer()
        else:
            print("config error ({})".format(self.model))
            sys.exit(1)
        


