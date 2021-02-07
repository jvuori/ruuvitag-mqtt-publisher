#!/bin/bash

ln -s `pwd`/ruuvitag-mqtt.service /etc/systemd/system/
systemctl enable ruuvitag-mqtt.service
