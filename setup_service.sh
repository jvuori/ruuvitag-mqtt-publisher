#!/bin/bash
set -e

cp ruuvitag-mqtt.service /etc/systemd/system/
cp -n ruuvitag_mqtt/ruuvitag-mqtt.json /etc

cp network-watchdog.sh /usr/local/sbin/
chmod +x /usr/local/sbin/network-watchdog.sh
cp network-watchdog.service /etc/systemd/system/

# Enable hardware watchdog via systemd (reboots if kernel/systemd hangs)
if ! grep -q 'RuntimeWatchdogSec' /etc/systemd/system.conf; then
    echo 'RuntimeWatchdogSec=15' >> /etc/systemd/system.conf
    echo 'RebootWatchdogSec=10min' >> /etc/systemd/system.conf
fi

systemctl daemon-reload
systemctl enable ruuvitag-mqtt.service
systemctl enable network-watchdog.service
systemctl start network-watchdog.service
