#!/bin/bash
# Reboots the device if the default gateway is unreachable for 3 consecutive checks (3 min).
GATEWAY=$(ip route show default | awk '/default/ {print $3; exit}')
FAIL=0
THRESHOLD=3

while true; do
    if [ -z "$GATEWAY" ]; then
        GATEWAY=$(ip route show default | awk '/default/ {print $3; exit}')
    fi

    if ping -c 2 -W 5 "$GATEWAY" > /dev/null 2>&1; then
        FAIL=0
    else
        FAIL=$((FAIL + 1))
        logger -t network-watchdog "Ping to $GATEWAY failed ($FAIL/$THRESHOLD)"
        if [ "$FAIL" -ge "$THRESHOLD" ]; then
            logger -t network-watchdog "Network unreachable after $THRESHOLD checks — rebooting"
            /sbin/reboot
        fi
    fi
    sleep 60
done
