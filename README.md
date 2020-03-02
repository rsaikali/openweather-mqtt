# openweather-mqtt

![PEP8](https://github.com/rsaikali/openweather-mqtt/workflows/PEP8/badge.svg)
![Docker](https://github.com/rsaikali/openweather-mqtt/workflows/Docker/badge.svg)

`openweather-mqtt` is a Python script to get weather from Openweather published to a MQTT (message queue) broker.

You'll need an Openweather account (free) and your city ID.

- [Openweather free account](https://home.openweathermap.org/users/sign_up)
- [Find your Openweather city ID](http://bulk.openweathermap.org/sample/city.list.json.gz)

As Openweather API calls are limited to 1 per 10 minutes, the application will re-publish same data every seconds, waiting for next API call.

## How to use it?

`openweather-mqtt` can be used as a standalone Python script or as a Docker container.

### Use as a standalone script

Git clone the project:

```sh
git clone https://github.com/rsaikali/openweather-mqtt.git
cd openweather-mqtt
```

Install Python requirements:

```sh
pip3 install -r requirements.txt
```

Configure through environment variables (those are default values if nothing given):

```sh
# Openweather account to use
export OPENWEATHER_APP_ID=<your application identifier>
# Openweather city identifier
export OPENWEATHER_CITY_ID=<your city identifier>

# MQTT broker host
export MQTT_SERVICE_HOST=mosquitto.local
# MQTT broker port
export MQTT_SERVICE_PORT=1883
# MQTT broker topic to publish measures
export MQTT_SERVICE_TOPIC=home/livingroom
# MQTT client ID (default will be the hostname)
export MQTT_CLIENT_ID=openweather-mqtt-service
```

Launch application:

```sh
python ./openweather_mqtt.py
```

You should see output printed:
```sh
2020-03-02 14:21:52,232 [openweather-mqtt-service]    DEBUG ################################################################################
2020-03-02 14:21:52,232 [openweather-mqtt-service]    DEBUG # OPENWEATHER_APP_ID=<your application identifier>
2020-03-02 14:21:52,232 [openweather-mqtt-service]    DEBUG # OPENWEATHER_CITY_ID=<your city identifier>
2020-03-02 14:21:52,232 [openweather-mqtt-service]    DEBUG # MQTT_SERVICE_HOST=mosquitto.local
2020-03-02 14:21:52,232 [openweather-mqtt-service]    DEBUG # MQTT_SERVICE_PORT=1883
2020-03-02 14:21:52,232 [openweather-mqtt-service]    DEBUG # MQTT_SERVICE_TOPIC=openweather
2020-03-02 14:21:52,232 [openweather-mqtt-service]    DEBUG # MQTT_CLIENT_ID=openweather-mqtt-service
2020-03-02 14:21:52,232 [openweather-mqtt-service]    DEBUG ################################################################################
2020-03-02 14:21:52,232 [openweather-mqtt-service]     INFO Connecting to OpenWeather for fresh weather information.
2020-03-02 14:21:52,239 [urllib3.connectionpool]    DEBUG Starting new HTTP connection (1): api.openweathermap.org:80
2020-03-02 14:21:52,291 [urllib3.connectionpool]    DEBUG http://api.openweathermap.org:80 "GET /data/2.5/weather?id=*******&appid=********************************&type=accurate&units=metric&lang=fr HTTP/1.1" 200 491
2020-03-02 14:21:52,293 [openweather-mqtt-service]     INFO base                     ---> stations
2020-03-02 14:21:52,293 [openweather-mqtt-service]     INFO clouds/all               ---> 100
2020-03-02 14:21:52,293 [openweather-mqtt-service]     INFO cod                      ---> 200
2020-03-02 14:21:52,293 [openweather-mqtt-service]     INFO coord/lat                ---> 47.34
2020-03-02 14:21:52,293 [openweather-mqtt-service]     INFO coord/lon                ---> 0.7
2020-03-02 14:21:52,293 [openweather-mqtt-service]     INFO dt                       ---> 1583154828
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO id                       ---> 3027343
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO main/feels_like          ---> 2.37
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO main/humidity            ---> 71
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO main/pressure            ---> 992
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO main/temp                ---> 9.36
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO main/temp_max            ---> 10.56
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO main/temp_min            ---> 7.78
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO name                     ---> Chambray-lès-Tours
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO rain/1h                  ---> 1.02
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO sys/country              ---> FR
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO sys/id                   ---> 6537
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO sys/sunrise              ---> 1583130913
2020-03-02 14:21:52,294 [openweather-mqtt-service]     INFO sys/sunset               ---> 1583171020
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO sys/type                 ---> 1
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO timezone                 ---> 3600
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO visibility               ---> 10000
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO weather/0/description    ---> pluie modérée
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO weather/0/icon           ---> 10d
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO weather/0/id             ---> 501
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO weather/0/main           ---> Rain
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO wind/deg                 ---> 280
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO wind/speed               ---> 8.2
2020-03-02 14:21:52,295 [openweather-mqtt-service]     INFO Publishing to mosquitto.local:1883
(...)
```

### Use as Docker container

#### Use Docker hub image

An image is available on Docker Hub: [rsaikali/openweather-mqtt](https://hub.docker.com/r/rsaikali/openweather-mqtt)

Needed environment is obviously the same as the standalone script mechanism, described in the Dockerfile:


```sh
docker run --name openweather-mqtt \
           --restart=always \
           --net=host \
           -tid \
           -e OPENWEATHER_APP_ID=<your application identifier> \
           -e OPENWEATHER_CITY_ID=<your city identifier> \
           -e MQTT_SERVICE_HOST=mosquitto.local \
           -e MQTT_SERVICE_PORT=1883 \
           -e MQTT_SERVICE_TOPIC=home/livingroom \
           -e MQTT_CLIENT_ID=dht22-mqtt-service \
           rsaikali/openweather-mqtt
```

#### Build your own Docker image

To build an `linux/arm/v7` docker image from another architecture, you'll need a special (experimental) Docker multi-architecture build functionality detailled here: [Building Multi-Arch Images for Arm and x86 with Docker Desktop](https://www.docker.com/blog/multi-arch-images/)

You'll basically need to activate experimental features and use `buildx`.

```sh
export DOCKER_CLI_EXPERIMENTAL=enabled
docker buildx create --use --name build --node build --driver-opt network=host
docker buildx build --platform linux/arm/v7 -t <your-repo>/openweather-mqtt --push .
```