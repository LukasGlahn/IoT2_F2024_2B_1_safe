from machine import I2C
import adafruit_sgp30
from dht import DHT11
from machine import Pin
import time
import ntptime

ntptime.settime()   

UTC_OFFSET = 1 * 60 * 60 
dht11 = DHT11(Pin(4, Pin.IN))
i2c = I2C(0)
led = Pin(23, Pin.OUT)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)


skoleid = 1
rumid = 1

sgp30.iaq_init()

print("Waiting 15 seconds for SGP30 & DHT11 initialization.")
time.sleep(15)

LUFTKVALITET_TOPIC = b'iot/data'

def connect_and_publish():
    global client_id, mqtt_server, LUFTKVALITET_TOPIC
    client = MQTTClient(client_id, mqtt_server)
    client.connect()
    print('Connected to %s MQTT broker' % mqtt_server)
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_publish()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        if (time.time() - last_message) > message_interval:
            dht11.measure()
            co2_eq, tvoc = sgp30.iaq_measure()
            now = time.localtime(time.time() + UTC_OFFSET)
            datetime = f'{now[2]}.{now[1]}.{now[0]}.{now[3]}:{"%02d" % (now[4])}'
            payload = f'luftkvalitet,{skoleid},{rumid},{dht11.temperature()},{dht11.humidity()},{co2_eq},{tvoc},{datetime}'
            payload = payload.encode('utf-8')
            client.publish(LUFTKVALITET_TOPIC, payload)
            led.value(1)
            last_message = time.time()
    except OSError as e:
        restart_and_reconnect()
led.value(0)
