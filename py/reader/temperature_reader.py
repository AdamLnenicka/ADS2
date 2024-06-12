from kafka import KafkaConsumer
import os
import time
from datetime import datetime

TOPIC = os.environ['TOPIC']
server = ['kafka:9092']  # Toto by mělo být konfigurovatelné z k8s manifestu pomocí ENV
HOSTNAME = os.environ['HOSTNAME']

consumer = KafkaConsumer(TOPIC, 
                         auto_offset_reset='latest',
                         bootstrap_servers=server)

try:
    for message in consumer:
        message = message.value.decode('utf-8')
        l = message.split(';')
        if len(l) != 2:
            print("Neplatný formát zprávy! Požadovaný formát: {nazev_mistnosti;teplota}")
            continue
        try:
            teplota = float(l[1])
        except ValueError:
            print("Neplatná hodnota teploty!")
            continue
        if 12.0 <= teplota <= 28.0:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Instance: {HOSTNAME} | Místnost: {l[0]} | Teplota: {teplota} °C")
        else:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Teplota mimo rozsah: {teplota} °C")

        time.sleep(2)

except IndexError:
    print("Chyba formátu zprávy! Požadovaný formát: {nazev_mistnosti;teplota}")
    consumer.close()

except KeyboardInterrupt:
    consumer.close()
