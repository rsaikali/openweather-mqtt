# -*- coding: utf-8 -*-
import logging
import os
import time

import paho.mqtt.publish as publish
import requests

# Config from environment (see Dockerfile)
OPENWEATHER_APP_ID = os.getenv('OPENWEATHER_APP_ID', 'YOUR_OPENWEATHER_APP_ID')
OPENWEATHER_CITY_ID = os.getenv('OPENWEATHER_CITY_ID', 'YOUR_OPENWEATHER_CITY_ID')

MQTT_SERVICE_HOST = os.getenv('MQTT_SERVICE_HOST', 'mosquitto.local')
MQTT_SERVICE_PORT = int(os.getenv('MQTT_SERVICE_PORT', 1883))
MQTT_SERVICE_TOPIC = os.getenv('MQTT_SERVICE_TOPIC', 'openweather')
MQTT_CLIENT_ID = os.getenv('HOSTNAME', 'openweather-mqtt-service')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(name)s] %(levelname)8s %(message)s')
logger = logging.getLogger(MQTT_CLIENT_ID)


def flatten_dict(dictionary, delimiter='.'):
    dictionary_ = dictionary

    def unpack(parent_key, parent_value):
        if isinstance(parent_value, dict):
            return [(parent_key + delimiter + key, value) for key, value in parent_value.items()]
        elif isinstance(parent_value, list):
            d = []
            for i, v in enumerate(parent_value):
                for k, vv in v.items():
                    d.append((parent_key + delimiter + str(i) + delimiter + k, vv))
            return d
        else:
            return [(parent_key, parent_value)]

    while True:
        dictionary_ = dict(ii for i in [unpack(key, value) for key, value in dictionary_.items()] for ii in i)
        if all([not isinstance(value, dict) for value in dictionary_.values()]):
            break

    return dictionary_


# Display config on startup
logger.debug("#" * 80)
logger.debug(f"# OPENWEATHER_APP_ID={OPENWEATHER_APP_ID}")
logger.debug(f"# OPENWEATHER_CITY_ID={OPENWEATHER_CITY_ID}")
logger.debug(f"# MQTT_SERVICE_HOST={MQTT_SERVICE_HOST}")
logger.debug(f"# MQTT_SERVICE_PORT={MQTT_SERVICE_PORT}")
logger.debug(f"# MQTT_SERVICE_TOPIC={MQTT_SERVICE_TOPIC}")
logger.debug(f"# MQTT_CLIENT_ID={MQTT_CLIENT_ID}")
logger.debug("#" * 80)

previous_last_update = 0
while True:
    try:

        logger.info("Connecting to OpenWeather for fresh weather information.")
        url = f"http://api.openweathermap.org/data/2.5/weather?id={OPENWEATHER_CITY_ID}&appid={OPENWEATHER_APP_ID}&type=accurate&units=metric&lang=fr"
        r = requests.get(url)
        data = r.json()

        # Hack: set default rain to 0 if no rain indicated
        data.setdefault('rain', {})
        data['rain'].setdefault('1h', 0)
        data['rain'].setdefault('3h', 0)

        if int(data['dt']) >= int(previous_last_update):
            previous_last_update = int(data['dt'])

            msgs = {}
            for k, v in sorted(flatten_dict(data, delimiter='/').items()):
                logger.info(f"{k:24} ---> {v}")
                msgs[f"{MQTT_SERVICE_TOPIC}/{k}"] = v
        else:
            logger.info("No updated data from Openweather...")

        # Publish openweather results on given MQTT broker every second, so we can view it often,
        # but call Openweather API every ~1min (otherwise you'll get locked due to API rate limits)
        last_update = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['dt']))
        for i in range(60):
            logger.info(f"Publishing to {MQTT_SERVICE_HOST}:{MQTT_SERVICE_PORT} [last_update={last_update}]")
            for k, v in msgs.items():
                publish.single(topic=k, payload=str(v), hostname=MQTT_SERVICE_HOST, port=MQTT_SERVICE_PORT, client_id=MQTT_CLIENT_ID)
            time.sleep(1)

    except Exception:
        logger.error("An error occured:", exc_info=True)
