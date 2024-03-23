from umqtt.simple import MQTTClient
from machine import Pin, reset
from time import sleep
from time import time

step1 = time()
# klient-setup til broker
CLIENT_NAME = 'Udluftnings-Lars'
BROKER_ADDR = ''
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR)
mqttc.connect()

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  reset()

# led setup
motor = Pin(32, Pin.OUT)
led = Pin(2, Pin.OUT)
UDLUFTNING_TOPIC = b'iot/udluftning'

def udluft(topic, msg):
    if msg.decode('utf-8') == 'sluk':
        motor.value(0)
        led.value(0)
    elif msg.decode('utf-8') == 'tænd':
        motor.value(1)
        led.value(1)
        
# mqtt subscription
mqttc.set_callback(udluft)
mqttc.subscribe(UDLUFTNING_TOPIC)

while True:
    try:
        mqttc.check_msg()
        sleep(0.5)
    except:
        step2 = time()
        print(step2 - step1)
        print(fail)
        restart_and_reconnect()
        
