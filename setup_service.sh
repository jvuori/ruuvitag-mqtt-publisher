#!/bin/bash

cp ruuvitag-mqtt.service /etc/systemd/system/
cp -n ruuvitag_mqtt/ruuvitag-mqtt.json /etc
systemctl enable ruuvitag-mqtt.service
