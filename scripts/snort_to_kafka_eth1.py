#!/usr/bin/env python3
"""
Snort to Kafka Alert Forwarder
WSL Architecture Version
"""
import json
import time
import sys
import socket
from kafka import KafkaProducer
from kafka.errors import KafkaError

WSL_IP = '172.28.254.81'
KAFKA_BROKER = f'{WSL_IP}:9092'
KAFKA_TOPIC = 'snort-alerts'
ALERT_FILE = '/var/log/snort_eth1/alert_json.txt'
SENSOR_ID = 'snort-sensor-02'
SENSOR_INTERFACE = 'eth1'
NETWORK_SEGMENT = 'seg-b'

def create_producer():
    """Create Kafka producer with retry logic"""
    retries = 0
    max_retries = 5
    
    while retries < max_retries:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=10000,
                max_block_ms=10000,
                retries=3
            )
            print(f"✅ Connected to Kafka at {KAFKA_BROKER}")
            return producer
        except KafkaError as e:
            retries += 1
            print(f"❌ Connection attempt {retries}/{max_retries} failed: {e}")
            if retries < max_retries:
                print(f"   Retrying in 5 seconds...")
                time.sleep(5)
    
    print("\n❌ Failed to connect to Kafka")
    print("\n📋 Troubleshooting:")
    print(f"   1. Is Kafka running on WSL? (WSL IP: {WSL_IP})")
    print("      → In WSL: jps | grep Kafka")
    print(f"   2. Can you reach WSL from Kali?")
    print(f"      → telnet {WSL_IP} 9092")
    print("   3. Check Windows Firewall allows port 9092")
    sys.exit(1)

def tail_file(filename):
    """Generator that yields new lines"""
    try:
        with open(filename, 'r') as f:
            f.seek(0, 2)
            print(f"📡 Monitoring {filename}...")
            
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                yield line
                
    except FileNotFoundError:
        print(f"\n❌ Alert file not found: {filename}")
        print("   Make sure Snort is running")
        sys.exit(1)

def main():
    hostname = socket.gethostname()
    
    print("="*70)
    print("🛡️  SNORT TO KAFKA FORWARDER (WSL Architecture)".center(70))
    print("="*70)
    print(f"📁 Alert file:      {ALERT_FILE}")
    print(f"🔗 Kafka broker:    {KAFKA_BROKER}")
    print(f"📨 Kafka topic:     {KAFKA_TOPIC}")
    print(f"🏷️  Sensor ID:       {SENSOR_ID}")
    print(f"🌐 Interface:       {SENSOR_INTERFACE}")
    print(f"📍 Segment:         {NETWORK_SEGMENT}")
    print(f"💻 Hostname:        {hostname}")
    print("="*70)
    print()
    
    producer = create_producer()
    alert_count = 0
    
    try:
        for line in tail_file(ALERT_FILE):
            try:
                alert = json.loads(line.strip())
                
                # Enrich metadata
                alert['sensor_id'] = SENSOR_ID
                alert['sensor_interface'] = SENSOR_INTERFACE
                alert['network_segment'] = NETWORK_SEGMENT
                alert['sensor_hostname'] = hostname
                alert['ingestion_timestamp'] = time.time()
                
                # Send to Kafka
                future = producer.send(KAFKA_TOPIC, value=alert)
                record_metadata = future.get(timeout=10)
                
                alert_count += 1
                
                msg = alert.get('msg', 'Unknown')
                src = alert.get('src_addr', '?')
                dst = alert.get('dst_addr', '?')
                proto = alert.get('proto', '?')
                
                print(f"✅ [{alert_count:04d}] [{NETWORK_SEGMENT}] {msg}")
                print(f"    └─ {src} → {dst} ({proto})")
                
            except json.JSONDecodeError:
                print(f"⚠️  Invalid JSON, skipping")
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except KeyboardInterrupt:
        print(f"\n\n🛑 Shutting down...")
        print(f"📊 Total alerts forwarded: {alert_count}")
    finally:
        producer.close()
        print("✅ Goodbye!")

if __name__ == "__main__":
    main()
