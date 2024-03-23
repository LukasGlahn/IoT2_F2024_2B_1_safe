import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from databace_conector import DataBase

ip = "mqtt serverIP"

# komonikaton
def get_mesege(ip):
    mqtt_payload = subscribe.simple("iot/database", hostname = ip)
    msg = mqtt_payload.payload.decode('utf-8')
    topic = mqtt_payload.topic
    return msg, topic

def send_mesege(ip,payload,feed):
    payload = payload.encode('utf-8')
    publish.single(feed, payload, hostname=ip)

database = DataBase("main_db.db")

komandoliste = {
    'luftkvalitet':{'sql_qury':"""INSERT INTO luftkvalitet (skoleid, rumid, temperature, humidity, co2, voc, datetime) VALUES(?, ?, ?, ?, ?, ?, ?)""",'data':7},
    'lyd':{'sql_qury':"""INSERT INTO luftkvalitet (skoleid, rumid, dba, datetime) VALUES(?, ?, ?, ?)""",'data':4},
}

while True:
    msg, top = get_mesege(ip)
    print(msg)
    print(top)
    data = msg.split(',')
    komando = data.pop(0)
    if komando == 'put':
        try:
            database_comand = komandoliste[data[0]]
            komando = data.pop(0)
            if len(data) == database_comand['data']:
                database.add_to_databace(database_comand['sql_qury'],data)
            else:
                print(f'the given list {data} did not fit the qury')

        except Exception as e:
            print(f'encounterd a error during add_to_databace: {e}')