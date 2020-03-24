import network
import time

from umqtt.simple import MQTTClient
from machine import Pin
import machine
import ubinascii

from config import CONFIG


# setup pin4 as output
pin = machine.Pin(4, machine.Pin.OUT)
pin.off() 
 

# process received messages
def onMessage(topic, msg):
    print("Topic: %s, message: %s" % (topic, msg))
    if msg == b"on":
        pin.on()
    elif msg == b"off":
        pin.off()
 

def listen():
    # create MQTTClient instance
    client_id = CONFIG['MQTT_CLIENT_ID_PREFIX'] + ubinascii.hexlify(machine.unique_id()).decode('utf-8')
    password = ubinascii.a2b_base64(CONFIG['MQTT_PASSWORD'])
    client = MQTTClient(client_id, CONFIG['MQTT_BROKER'], user=CONFIG['MQTT_USER'], password=password, port=CONFIG['MQTT_PORT'])
    # attach call back handler to be called on received messages
    client.set_callback(onMessage)
    client.connect()
    # client.publish("ping", "ESP8266 is connected")
    client.subscribe(CONFIG['MQTT_TOPIC'])
    print("ESP8266 is connected to '%s' and subscribed to '%s' topic" % (CONFIG['MQTT_BROKER'], CONFIG['MQTT_TOPIC']))
 
    try:
        while True:
            msg = client.wait_msg()
    finally:
        client.disconnect()  

sta_if = network.WLAN(network.STA_IF)


# connect to Wifi
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


# start service
time.sleep(1)
listen()
