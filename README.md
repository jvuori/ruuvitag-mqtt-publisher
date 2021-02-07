# ruuvitag_mqtt

RuuviTag MQTT Publisher. Designed for Raspberry Pi Zero W.

# Install

## Libs and the actual service

Install prerequisites by following the instructions here:
https://github.com/ttu/ruuvitag-sensor

Then clone the repo and run installation procedure:

    git clone https://github.com/jvuori/ruuvitag-mqtt-publisher.git

    cd ruuvitag-mqtt-publisher

    sudo python3 -m pip install .
    sudo ./setup_service.sh

The setup script creates a Systemd setup file and enables the ```ruuvitag-mqtt.service``` to start automatically on startup.

Note: For now _RuuviTag MQTT Publisher_ can't be run without ```sudo```. The restriction comes from ruuvitag-sensor library which uses ```sudo``` internally.


## Configuration

Modify config file: ```/etc/ruuvitag-mqtt.conf```

Example:

```json
    {
        "broker": {
            "host": "192.168.1.11",
            "port": 1883
        },
        "ruuvitags": {
            "DE:D4:96:2C:3C:78": {
                "name": "kitchen",
                "fields": ["temperature", "humidity"]
            },
            "E3:35:52:F1:D2:AA": {
                "name": "terrace",
                "fields": ["temperature", "humidity", "pressure"]
            },
            "F9:89:71:39:A5:82": {
                "name": "sauna",
                "fields": ["temperature", "humidity"]
            }
        }
    }
```


## Start service

    systemctl start ruuvitag-mqtt.service


# Troubleshooting

Run _RuuviTag MQTT Publisher_ from terminal:

    sudo python3 -m ruuvitag_mqtt -c my_config_file.json


# Alternatives and inspiration

[ruuvi2mqtt](https://github.com/ppetru/ruuvi2mqtt) is another publisher service written with Node.js. Seems to be supporting MQTT Discovery.

[Basic MQTT publisher for Ruuvitags](https://f.ruuvi.com/t/basic-mqtt-publisher-for-ruuvitags/3978): Python code snippet found in [Ruuvi Forum](https://f.ruuvi.com/).

[post_to_mqtt.py](https://github.com/ttu/ruuvitag-sensor/blob/master/examples/post_to_mqtt.py): Example script where configuration is based on various command line arguments.
