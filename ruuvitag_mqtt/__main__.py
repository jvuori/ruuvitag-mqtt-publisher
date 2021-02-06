from paho.mqtt import client
from ruuvitag_sensor.ruuvi import RuuviTagSensor


mqtt_client = client.Client("RuuviTag")
mqtt_client.connect("192.168.1.11", )
mqtt_client.disconnect()

mac_location_map = {
    "DE:D4:96:2C:3C:78": "kitchen",
    "E3:35:52:F1:D2:AA": "terrace",
    "F9:89:71:39:A5:82": "sauna",
}

valid_keys = [
    "temperature",
    "humidity",
]

def on_ruuvi_event(ruuvi_event):
    mac_address, data = ruuvi_event
    location = mac_location_map.get(mac_address)
    if location:
        mqtt_client.reconnect()
        for key, value in data.items():
            if key in valid_keys:
                mqtt_client.publish(f"home/{location}/{key}", value)
        mqtt_client.disconnect()


def start_publishing():
    RuuviTagSensor.get_datas(on_ruuvi_event)

if __name__ == '__main__':
    start_publishing()