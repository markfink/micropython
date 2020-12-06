import network
from time import sleep

from umqtt.simple import MQTTClient
from machine import Pin, I2C
import ubinascii
import onewire, ds18x20

import bme280
import ds18b20
from config import CONFIG


# ESP32 pins
#i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
# ESP8266 pins
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)


# connect to Wifi
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    password = ubinascii.a2b_base64(CONFIG['NETWORK_PASSWORD'])
    sta_if.connect(CONFIG['NETWORK_SSID'], password)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())


# disable Access-Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)



def serve():
    bme = bme280.BME280(i2c=i2c)
    # create the onewire object
    ds = ds18x20.DS18X20(onewire.OneWire(Pin(2)))  # the ds18b20 is on GPIO4
    # mqtt client
    client_id = CONFIG['MQTT_CLIENT_ID_PREFIX'] + ubinascii.hexlify(machine.unique_id()).decode('utf-8')
    password = ubinascii.a2b_base64(CONFIG['MQTT_PASSWORD'])
    client = MQTTClient(client_id, CONFIG['MQTT_BROKER'], user=CONFIG['MQTT_USER'], password=password, port=CONFIG['MQTT_PORT'])
    client.connect()
    print("'%s' is connected to '%s'" % (client_id, CONFIG['MQTT_BROKER']))

    while True:
        temp = bme.temperature
        hum = bme.humidity
        pres = bme.pressure

	temps = ds18b20.read_temperatures(ds)

        # publish the values
        client.publish("%s.temp_c" % client_id, temp)
        client.publish("%s.humidity_rh" % client_id, hum)
        client.publish("%s.pressure_hpa" % client_id, pres)
        for serial_nbr, temp in temps.items():
            client.publish("%s.%s.temp_c" % (client_id, serial_nbr), '%0.5f' % temp)


        sleep(300)


sleep(1)
serve()
