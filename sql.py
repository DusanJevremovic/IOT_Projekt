import json
import sqlite3
import paho.mqtt.client as mqtt
 
DB_NAME = "sensor_data.db"
 
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
 
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raspi_id TEXT,
    sensor TEXT,
    value TEXT,
    timestamp TEXT
)
""")
conn.commit()
 
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
 
    raspi_id = data["raspi_id"]
    sensor = data["sensor"]
    timestamp = data["timestamp"]
 
    # Kamera oder IR unterscheiden
    if sensor == "ir":
        value = data["value"]
    else:
        value = data["text"]
 
    cursor.execute(
        "INSERT INTO sensor_data (raspi_id, sensor, value, timestamp) VALUES (?, ?, ?, ?)",
        (raspi_id, sensor, value, timestamp)
    )
    conn.commit()
 
    print("Gespeichert:", data)
 
client = mqtt.Client()
client.on_message = on_message
 
client.connect("localhost", 1883, 60)
client.subscribe("sensors/#")
 
client.loop_forever()