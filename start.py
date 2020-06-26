import sys

from app.loader import EnergyReader

# MAIN: Setup of the project
if __name__ == "__main__":

    if(len(sys.argv)>1):
        CONFIG_PATH = sys.argv[1]
    else:
        CONFIG_PATH = './config'

    EnergyReader(CONFIG_PATH)

    # schema = {
    #     "type" : "object",
    #     "properties": {
    #         "tag": { "type": "string" },
    #         "address": { "type": "number" },
    #         "port": { "type": "string" },
    #         "mode": { "type": "string" },
    #         "baudrate": { "type": "number" },
    #         "timeout": { "type": "number" },
    #         "sleep-response": { "type": "number" },
    #         "commands": { "type": "object" }
    #     }
    # }

    # parser = ArgumentParser()
    # parser.add_argument('--op', action=ActionJsonSchema(schema=schema))
    # parser.parse_args(['--op', 'config/meters/config_SDM120.json'])
