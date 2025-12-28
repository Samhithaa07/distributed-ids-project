# Setup Instructions

## Prerequisites
- Windows 10/11 with WSL2 enabled
- Oracle VirtualBox installed
- 16GB RAM minimum
- 60GB free disk space

## Quick Start

### 1. Start WSL SIEM Server
```bash
cd ~/kafka/kafka-current
./bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
./bin/kafka-server-start.sh -daemon config/server.properties
sudo systemctl start elasticsearch logstash kibana
```

### 2. Start Kali Sensors
```bash
./start-sensors.sh
```

### 3. Access Kibana
Open browser: http://localhost:5601

## Detailed Setup
See main README.md for complete installation guide.
