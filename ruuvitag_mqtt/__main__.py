import os
import argparse
from pathlib import Path
import json
import logging
import time

os.environ["RUUVI_BLE_ADAPTER"] = "bleak"

from paho.mqtt import client as mqtt
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from ruuvitag_sensor import adapters
import asyncio

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

adapter = adapters.get_ble_adapter()
logger.info("Using BLE adapter: %s", adapter)


mqtt_client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="RuuviTag",
)


def on_ruuvi_event(ruuvi_event):
    mac_address, data = ruuvi_event
    configured_ruuvitags = config.get("ruuvitags", {})
    location = configured_ruuvitags.get(mac_address, {}).get("name", mac_address)
    topic_prefix = config.get("topic_prefix", "")
    mqtt_client.reconnect()
    for key, value in data.items():
        fields = configured_ruuvitags.get(mac_address, {}).get("fields")
        retain = configured_ruuvitags.get(mac_address, {}).get("retain", False)
        if fields is None or key in fields:
            mqtt_client.publish(
                f"{topic_prefix}{location}/{key}",
                value,
                retain=retain,
            )
    mqtt_client.disconnect()


async def start_publishing(config_file_path: Path):
    global config, mqtt_client

    logger.info("Using config file: %s", config_file_path)

    if not config_file_path:
        config_file_path = Path(__file__).parent / "ruuvitag-mqtt.json"
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    print(config)

    logger.info("Connecting to MQTT broker")
    retry_count = 0
    while retry_count < 10:
        try:
            username = config.get("broker", {}).get("username")
            if username:
                logger.info("Using authentication: %s", username)
                password = config.get("broker", {}).get("password")
                mqtt_client.username_pw_set(username=username, password=password)

            mqtt_client.connect(
                host=config.get("broker", {}).get("host", "localhost"),
                port=config.get("broker", {}).get("port", 1883),
            )
            break
        except OSError as e:
            logger.error("Failed to connect to MQTT broker: %s", e)
            logger.info("Retrying in 10 seconds. Retry count: %d", retry_count + 1)
            retry_count += 1
            time.sleep(10)
            del mqtt_client
            mqtt_client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id="RuuviTag",
            )

    else:
        msg = "Failed to connect to MQTT broker after multiple retries. Exiting..."
        raise ConnectionError(msg)
    logger.info("Connected to MQTT broker")

    mqtt_client.disconnect()

    async for ruuvi_event in RuuviTagSensor.get_data_async():
        on_ruuvi_event(ruuvi_event)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-c", dest="config_file")
    args = argument_parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_publishing(args.config_file))
