import paho.mqtt.client as mqtt
import json
import time
import random
import socket

student_name = "Akshaya TV"
unique_id = "42130615"

# MQTT Configuration
broker_address = "localhost"  # Change if your broker is on a different machine
broker_port = 1883
topic = f"home/{student_name.lower().replace(' ', '-')}-2025/sensor"

# Create a client instance
client = mqtt.Client(client_id=f"{student_name.replace(' ', '')}_{unique_id}")

# Connect to the broker
try:
    client.connect(broker_address, broker_port, 60)
    print(f"Connected to MQTT broker at {broker_address}:{broker_port}")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Function to publish sensor data
def publish_sensor_data():
    # Create sensor data
    sensor_data = {
        "temperature": 25,  # Fixed temperature as required
        "humidity": 60,      # Fixed humidity as required
        "light": random.randint(200, 800),  # Extra sensor: light level in lux (random for demo)
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "student_name": student_name,
        "unique_id": unique_id
    }
    
    # Convert to JSON
    payload = json.dumps(sensor_data)
    
    # Publish to the topic
    result = client.publish(topic, payload)
    status = result[0]
    
    if status == 0:
        print(f"Sent sensor data to topic: {topic}")
        print(f"Data: {payload}")
    else:
        print(f"Failed to send message to topic {topic}")
    
    return status

# Get local IP for additional identification
try:
    local_ip = socket.gethostbyname(socket.gethostname())
except:
    local_ip = "127.0.0.1"

print(f"Starting MQTT publisher for {student_name} ({unique_id})")
print(f"Local IP: {local_ip}")
print(f"Publishing to topic: {topic}")
print("Press Ctrl+C to stop")

# Main loop - publish data every 5 seconds
try:
    while True:
        publish_sensor_data()
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping publisher...")
    client.disconnect()