import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

import json
import time

#Creates a global logger used for every object of the "Device" class
#Creating local loggers for every object produce collisions
# logger = modbus_tk.utils.create_logger("console")  #modbus_tk's logger

class Device():

    def __init__(self, configFile):
        with open(configFile) as json_file:
            self.config = json.load(json_file) #Config parametes for the device
        # self.logger = modbus_tk.utils.create_logger("console")  #modbus_tk's logger
        self.supported_types = ["IEEE"]

    def open(self):
        #Check if the mode is 'rtu'
        self.mode = self.config["mode"]
        if(self.mode != "rtu"):
            raise RaiseError("'rtu' mode is the only one supported")

        #Parameters needed to start the communication with the device
        self.port = self.config["port"]
        self.baudrate = self.config["baudrate"]
        self.timeout = self.config["timeout"]

        self.device = modbus_rtu.RtuMaster(
            serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )

        self.device.set_timeout(self.timeout)
        self.device.set_verbose(True)
        # logger.info("connected")


    def execute(self, command):
        #Verify if the command exists in the configuration file
        try:
            comm_param = self.config["commands"][command]
        except Exception as exc:
            raise RaiseError("'{}' command not exists in the config file".format(command))

        #Command options
        address = self.config["address"]
        signed = comm_param["signed"]
        register = comm_param["register"]
        type = comm_param["type"]
        fnCode = comm_param["fn-code"]
        unit = comm_param["unit"]

        #Seconds of sleep after response from slave
        # *This is needed in order to be able to send the next request without having conflicts
        sleep_response = self.config["sleep-response"]

        #Check if type is supported
        if(type not in self.supported_types):
            raise RaiseError("{} is not supported".format(type))

        if(type == "IEEE"):
            try:
                data = (self.device.execute(slave=address, function_code=fnCode, starting_address=int(register, 16), quantity_of_x=2, data_format=">f"))
                time.sleep(sleep_response)
                return data[0]
            except Exception as exc:
                print("Oops! Something wrong happened: {}".format(exc))
                return None


class RaiseError(Exception):
    def __init__(self, message):
        print(message)
