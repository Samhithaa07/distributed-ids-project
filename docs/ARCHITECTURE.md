# System Architecture

## Component Distribution

### WSL (SIEM Server)
- Apache Kafka 3.9.0
- Elasticsearch 8.x
- Logstash 8.x
- Kibana 8.x

### Kali VM (Sensor)
- Snort 3.x (2 instances)
- Python forwarders (2 instances)

## Data Flow
1. Snort detects traffic → Writes JSON alerts
2. Python forwarder → Reads JSON → Sends to Kafka
3. Kafka → Queues alerts
4. Logstash → Consumes from Kafka → Enriches data
5. Elasticsearch → Indexes alerts
6. Kibana → Visualizes data

## Network Layout
See network-topology.png
