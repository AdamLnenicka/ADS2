from kafka import KafkaProducer
import os
import time
import random

TOPIC = 'temperature'
server = ['kafka:9092']  # This should be configurable similarly to your consumer

producer = KafkaProducer(bootstrap_servers=server, 
                         value_serializer=lambda v: v.encode('utf-8'))

room_names = ['kuchyně', 'obývací_pokoj', 'ložnice', 'koupelna', 'garáž', 'chodba', 'venku']

try:
    while True:
        room_name = random.choice(room_names)
        temperature = round(random.uniform(12.0, 28.0), 1)  # Generate a random temperature between 12.0 and 28.0
        message = f"{room_name};{temperature}"
        producer.send(TOPIC, message)
        print(f"Sent message: {message}")
        time.sleep(2)  # Wait for 2 seconds before sending the next message

except KeyboardInterrupt:
    producer.close()
