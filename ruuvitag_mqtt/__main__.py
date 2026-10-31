import argparse
from pathlib import Path
import json
import logging
import time
import multiprocessing

# Use nix_hci (sync) adapter - bleak stops scanning after ~11s on BCM43430/Pi Zero W
# due to combined Wi-Fi+BT UART contention. nix_hci uses passive hcitool/hcidump
# which is stable on this hardware.

# _NoOpList: prevent MAC blacklisting so a single bad parse doesn't silence a tag.
# Manager().list() is replaced to avoid IPC overhead (was stalling event loop in
# the old bleak path; kept here for consistency even in sync context).
class _NoOpList(list):
    def append(self, *a): pass
    def __contains__(self, item): return False

class _LocalManager:
    def start(self): pass
    def shutdown(self): pass
    def list(self): return _NoOpList()

multiprocessing.Manager = _LocalManager

from paho.mqtt import client as mqtt
from ruuvitag_sensor.ruuvi import RuuviTagSensor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = {}
mqtt_client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="RuuviTag-sauna",
)


def on_ruuvi_event(ruuvi_event):
    mac_address, data = ruuvi_event
    configured_ruuvitags = config.get("ruuvitags", {})
    location = configured_ruuvitags.get(mac_address, {}).get("name", mac_address)
    topic_prefix = config.get("topic_prefix", "")
    fields = configured_ruuvitags.get(mac_address, {}).get("fields")
    retain = configured_ruuvitags.get(mac_address, {}).get("retain", False)

    try:
        mqtt_client.reconnect()
        for key, value in data.items():
            if value is not None and (fields is None or key in fields):
                mqtt_client.publish(
                    f"{topic_prefix}{location}/{key}",
                    value,
                    retain=retain,
                )
        mqtt_client.loop_write()
    except Exception as e:
        logger.error("MQTT publish error: %s", e)
    finally:
        try:
            mqtt_client.disconnect()
        except Exception:
            pass


def start_publishing(config_file_path: Path):
    global config, mqtt_client

    if not config_file_path:
        config_file_path = Path(__file__).parent / "ruuvitag-mqtt.json"
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    logger.info("Config: %s", config)

    logger.info("Connecting to MQTT broker")
    retry_count = 0
    while retry_count < 10:
        try:
            username = config.get("broker", {}).get("username")
            if username:
                password = config.get("broker", {}).get("password")
                mqtt_client.username_pw_set(username=username, password=password)
            mqtt_client.connect(
                host=config.get("broker", {}).get("host", "localhost"),
                port=config.get("broker", {}).get("port", 1883),
            )
            break
        except OSError as e:
            logger.error("Failed to connect to MQTT broker: %s", e)
            retry_count += 1
            time.sleep(10)
            del mqtt_client
            mqtt_client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id="RuuviTag-sauna",
            )
    else:
        msg = "Failed to connect to MQTT broker after multiple retries. Exiting..."
        raise ConnectionError(msg)
    logger.info("Connected to MQTT broker, starting BLE scan")
    mqtt_client.disconnect()

    RuuviTagSensor.get_data(on_ruuvi_event)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-c", dest="config_file")
    args = argument_parser.parse_args()
    start_publishing(args.config_file)
