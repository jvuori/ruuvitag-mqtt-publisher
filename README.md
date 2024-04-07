# RuuviTag MQTT Publisher

Publishes [RuuviTag](https://ruuvi.com/) events to [MQTT](https://mqtt.org/) broker. Designed to run on [Raspberry Pi](https://www.raspberrypi.org/) devices having [Bluetooth LE](https://en.wikipedia.org/wiki/Bluetooth_Low_Energy) capabilities, for example [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero/).

# Installation

## Libs and the actual service

Install prerequisites by following the instructions here:
https://github.com/ttu/ruuvitag-sensor

Then clone the repo and run installation procedure:

    git clone https://github.com/jvuori/ruuvitag-mqtt-publisher.git

    cd ruuvitag-mqtt-publisher

    sudo python3 -m pip install .
    sudo ./setup_service.sh

The setup script creates a [Systemd](https://www.freedesktop.org/wiki/Software/systemd/) setup file and enables the `ruuvitag-mqtt.service` to start automatically on startup.

Note: For now _RuuviTag MQTT Publisher_ can't be run without `sudo`. The restriction comes from ruuvitag-sensor library which uses `sudo` internally.

## Configuration

Modify config file: `/etc/ruuvitag-mqtt.json`

Example:

```json
{
    "broker": {
        "host": "192.168.1.11",
        "port": 1883,
        "username": null,
        "password": null
    },
    "topic_prefix": "myhome/",
    "ruuvitags": {
        "DE:D4:96:2C:3C:78": {
            "name": "kitchen",
            "retain": false,
            "fields": ["temperature", "humidity"]
        },
        "E3:35:52:F1:D2:AA": {
            "name": "terrace",
            "retain": false,
            "fields": ["temperature", "humidity", "pressure"]
        },
        "F9:89:71:39:A5:82": {
            "name": "sauna",
            "retain": false,
            "fields": ["temperature", "humidity"]
        }
    }
}
```

The above example will publish the following MQTT topics:

-   myhome/kitchen/temperature
-   myhome/kitchen/humidity
-   myhome/terrace/temperature
-   myhome/terrace/humidity
-   myhome/terrace/pressure
-   myhome/sauna/temperature
-   myhome/sauna/humidity

## Start service

    systemctl start ruuvitag-mqtt.service

# Troubleshooting

Run _RuuviTag MQTT Publisher_ from terminal:

    sudo python3 -m ruuvitag_mqtt -c my_config_file.json

# Alternatives and inspiration

[ruuvi2mqtt](https://github.com/ppetru/ruuvi2mqtt) is another publisher service written with Node.js. Seems to be supporting MQTT Discovery.

[Basic MQTT publisher for Ruuvitags](https://f.ruuvi.com/t/basic-mqtt-publisher-for-ruuvitags/3978): Python code snippet found in [Ruuvi Forum](https://f.ruuvi.com/).

[post_to_mqtt.py](https://github.com/ttu/ruuvitag-sensor/blob/master/examples/post_to_mqtt.py): Example script where configuration is based on various command line arguments.
