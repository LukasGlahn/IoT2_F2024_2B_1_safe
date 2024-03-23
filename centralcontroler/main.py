import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import sqlite3
from time import sleep

ip = ""
udluftning_tænt = False

# komonikaton
def get_mesege(ip):
    mqtt_payload = subscribe.simple("iot/#", hostname = ip)
    msg = mqtt_payload.payload.decode('utf-8')
    topic = mqtt_payload.topic
    return msg, topic

def send_mesege(ip,payload,feed):
    payload = payload.encode('utf-8')
    publish.single(feed, payload, hostname=ip)

#databace
def add_to_databace(query,data):
    try:
        conn = sqlite3.connect("database/database.db")
        cur = conn.cursor()
        cur.execute(query,data)
        conn.commit()

    except sqlite3.Error as sql_e:
        print(f'sqlite encounterd a error: {sql_e}')
        conn.rollback()

    except Exception as e:
        print(f'encounterd a error: {e}')

    finally:
        conn.close()


def get_databace_data(query,max_output = 20):
    try:
        conn = sqlite3.connect("database/database.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(max_output)
        return rows

    except sqlite3.Error as sql_e:
        print(f'sqlite encounterd a error: {sql_e}')
        conn.rollback()

    except Exception as e:
        print(f'encounterd a error: {e}')

    finally:
        conn.close()

#other
def udlufter_logik(data):
    global udluftning_tænt
    værdier = data[2:6]
    tæler = 3
    er_over = []
    rows = get_databace_data('''SELECT * FROM rum_værdier WHERE id IS 1''',1)
    for row in rows:
        max_senser_værdi = row
    for værdi in værdier:
        if int(værdi) > max_senser_værdi[tæler]:
            er_over.append(1)
        else:
            er_over.append(0)
        tæler += 1
    overskedet_luft_værdi = sum(er_over) > 0
    if not udluftning_tænt and overskedet_luft_værdi:
        sleep(0.2)
        send_mesege(ip,'tænd','iot/udluftning')
        print('tænder for udluft')
        udluftning_tænt = True
    elif udluftning_tænt and not overskedet_luft_værdi:
        sleep(0.2)
        send_mesege(ip,'sluk','iot/udluftning')
        print('slukker for udluft')
        udluftning_tænt = False

def ændre_rum_værdier(data):
    qury = """UPDATE rum_værdier SET (temperatur, humitity, co2, voc) = (?,?,?,?) WHERE id = 1;"""
    værdier = (data[1],data[2],data[3],data[4])
    add_to_databace(qury,værdier)
    

def database_comand_constructer(data):
    ...


komandoliste = {
    'luftkvalitet':{'sql_qury':"""INSERT INTO luftkvalitet (skoleid, rumid, temperatur, humitity, co2, voc, datetime) VALUES(?, ?, ?, ?, ?, ?, ?)""",'data':7},
    'lyd':{'sql_qury':"""INSERT INTO luftkvalitet (skoleid, rumid, dba, datetime) VALUES(?, ?, ?, ?)""",'data':4},
}


#main loop
while True:
    msg, top = get_mesege(ip)
    print(msg)
    print(top)
    data = msg.split(',')
    if top == 'iot/data':
        try:
            database_comand = komandoliste[data[0]]
            komando = data.pop(0)
            if len(data) == database_comand['data']:
                add_to_databace(database_comand['sql_qury'],data)
                send_mesege(ip,f'put,{msg}','iot/database')
            else:
                print(f'the given list {data} did not fit the qury')

        except Exception as e:
            print(f'encounterd a error during add_to_databace: {e}')
        try:
            if komando == 'luftkvalitet':
                try:
                    udlufter_logik(data)
                except Exception as e:
                    print(f'encounterd a error during udlufter_logik: {e}')
                komando = None
        except:
            print(f'encounterd a error during add_to_databace: {e}')

    if top == 'iot/komando':
        if data[0] == 'ændre_rum_værdier':
            ændre_rum_værdier(data)
        