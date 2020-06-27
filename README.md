# pi-energy-reader
Schedule data collection from energy meters connected to a Raspberry Pi and push it to an MQTT Broker.
  - Supports MODBUS energy meters
  - No need to write custom code to use it
  - MQTT Integrated
  - Lightweight

# Getting started
This project is designed to work on a Raspberry Pi. It has only been tested on a Raspberry Pi 3 B+, but it should work on any version of the board.

## Installation
Fist of all, clone the project somewhere in your system and ```cd``` into it.
```
git clone https://github.com/samueleallegranza/pi-energy-reader.git
```

For the project dependencies, it's reccomended to use a Python3 virtual environment. You'll need to install ```virtualenv``` from pip. Then create a virtualenv folder inside the project's folder, activate the environment and download all the dependencies contained in ```requirements.txt```
```
pip3 install virtualenv
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
```
To deactivate the virtualenv use the ```deactivate``` command

### Run on startup
Once you tested the project and got it up and running, the need to run the project on boot may arise. This way, you won't need to restart everything manually every time the power goes out.

To achieve this, is necessary to run the project as a service on linux (```systemd```). An example of ```.service``` file has been already created and tested for you, you can find it in ```examples/energyReader.service```. 
All you need to do is to adjust the paths with yours. Then copy the file into the systemd directory and reload:

**[!]** The use of **absolute paths** is highy recommended
```
cp examples/energyReader.service /etc/systemd/system/
sudo systemctl daemon-reload
```
To start the service use
```
sudo systemctl start energyReader.service
```
To check its status use
```
sudo systemctl status energyReader.service
```
If you need to restart the service for some reasons, use
```
sudo systemctl restart energyReader.service
```

# How to use
Work in progress
# To-do
Work in progress
# Author
Work in progress
