#!/bin/bash
set -e

cp ruuvitag-mqtt.service /etc/systemd/system/
cp -n ruuvitag_mqtt/ruuvitag-mqtt.json /etc

cp network-watchdog.sh /usr/local/sbin/
chmod +x /usr/local/sbin/network-watchdog.sh
cp network-watchdog.service /etc/systemd/system/

# Enable hardware watchdog via systemd drop-in (reboots if kernel/systemd hangs)
mkdir -p /etc/systemd/system.conf.d
cat > /etc/systemd/system.conf.d/watchdog.conf << 'WATCHDOG'
[Manager]
RuntimeWatchdogSec=15
RebootWatchdogSec=10min
WATCHDOG

systemctl daemon-reload
systemctl daemon-reexec
systemctl enable ruuvitag-mqtt.service
systemctl enable network-watchdog.service
systemctl start network-watchdog.service
