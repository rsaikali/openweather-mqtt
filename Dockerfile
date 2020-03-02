FROM python:alpine

ENV OPENWEATHER_APP_ID YOUR_OPENWEATHER_APP_ID
ENV OPENWEATHER_CITY_ID YOUR_OPENWEATHER_CITY_ID

ENV MQTT_SERVICE_HOST mosquitto.local
ENV MQTT_SERVICE_PORT 1883
ENV MQTT_SERVICE_TOPIC home/livingroom
ENV MQTT_CLIENT_ID openweather-mqtt-service

RUN apk add -U tzdata
RUN cp /usr/share/zoneinfo/Europe/Paris /etc/localtime

WORKDIR /opt

COPY requirements.txt /opt/requirements.txt

RUN pip3 install --no-cache-dir -r /opt/requirements.txt

COPY openweather_mqtt.py /opt/openweather_mqtt.py

ENTRYPOINT ["python", "/opt/openweather_mqtt.py"]