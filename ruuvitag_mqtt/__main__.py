import argparse
from pathlib import Path
import json
import logging

from paho.mqtt import client as mqtt
from paho.mqtt.properties import Properties, PacketTypes
from ruuvitag_sensor.ruuvi import RuuviTagSensor

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

mqtt_client = mqtt.Client("RuuviTag")


def on_ruuvi_event(ruuvi_event):
    mac_address, data = ruuvi_event
    configured_ruuvitags = config.get("ruuvitags", {})
    location = configured_ruuvitags.get(mac_address, {}).get("name", mac_address)

    mqtt_client.reconnect()
    for key, value in data.items():
        fields = configured_ruuvitags.get(mac_address, {}).get("fields")
        if fields is None or key in fields:
            mqtt_client.publish(
                f"home/{location}/{key}",
                value,
            )
    mqtt_client.disconnect()


def start_publishing(config_file_path: Path):
    global config

    logger.info("Using config file: %s", config_file_path)

    if not config_file_path:
        config_file_path = Path(__file__).parent / "ruuvitag_mqtt.json"
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    print(config)

    mqtt_client.connect(
        host=config.get("broker", {}).get("host", "localhost"),
        port=config.get("broker", {}).get("port", 1883),
    )
    mqtt_client.disconnect()

    RuuviTagSensor.get_datas(on_ruuvi_event)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-c", dest="config_file")
    args = argument_parser.parse_args()

    start_publishing(args.config_file)