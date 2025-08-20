from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime
from configparser import ConfigParser

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

zones = ['Downtown', 'Suburb', 'Airport', 'Uptown']

print("Starting producer...")
i=0
while True:
    event = {
        'timestamp': datetime.now().isoformat(),
        'zone': random.choice(zones),
        'cost': round(random.uniform(10, 50), 2),
        'status': random.choice(['booked', 'tracking', 'completed'])
    }
    producer.send('uber_events', event)
    producer.flush()
    print(f"Sent: {event}")
    time.sleep(1)
    i=i+1