from kafka import KafkaConsumer
import json
from configparser import ConfigParser
import mysql.connector
from collections import Counter
from datetime import datetime, timedelta

config = ConfigParser()

consumer = KafkaConsumer(
    'uber_events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='uber_group'
)

conn = mysql.connector.connect(
    host='localhost',
    user=config['db']['user_name'],
    password=config['db']['password'],
    database='uber_db'
)
cur = conn.cursor()

insights = Counter()

print("Starting consumer...")
for msg in consumer:
    event = msg.value
    # Insert into MySQL
    cur.execute(
        "INSERT INTO bookings (timestamp, zone, cost, status) VALUES (%s, %s, %s, %s)",
        (event['timestamp'], event['zone'], event['cost'], event['status'])
    )
    conn.commit()
    
    # Aggregate for insights
    event_time = datetime.fromisoformat(event['timestamp'])
    if event_time > datetime.now() - timedelta(minutes=5):
        insights[event['zone']] += 1
    
    major_zone = insights.most_common(1)[0][0] if insights else 'None'
    print(f"Major zone: {major_zone}")