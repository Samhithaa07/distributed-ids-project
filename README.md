# Distributed Intrusion Detection System

## Implementation using Snort, Apache Kafka, and ELK Stack



A production-grade distributed intrusion detection system demonstrating real-time threat detection, message streaming, and data visualization across multiple network segments.



---



## Table of Contents



- Overview

- Architecture

- Features

- System Requirements

- Technology Stack

- Project Structure

- Installation Guide

- Configuration
  
- Usage

- Testing and Validation

- Dashboard and Visualization

- Results

- Challenges and Solutions

- Troubleshooting

- Future Enhancements

- Contributing

- License

- Acknowledgments



---



## Overview



This project implements a distributed intrusion detection system capable of monitoring multiple network segments simultaneously. The system uses Snort for packet analysis, Apache Kafka for reliable message streaming, and the ELK Stack (Elasticsearch, Logstash, Kibana) for data processing and visualization.



### Key Innovation



This implementation uses a hybrid architecture combining Windows Subsystem for Linux (WSL) and VirtualBox virtual machines to optimize resource utilization while maintaining network monitoring flexibility. The SIEM components run on WSL, consuming approximately 2.5GB RAM, while Snort sensors operate in isolated Kali Linux virtual machines.



### Use Cases



\- Small business network security monitoring

\- Educational demonstrations of distributed IDS architecture

\- Security research and testing environments

\- Proof-of-concept for enterprise IDS deployments



---



## Architecture



The system consists of three primary components distributed across WSL and two VirtualBox virtual machines:



### Component Distribution



**SIEM Server (WSL Ubuntu)**

\- Apache Kafka: Message broker receiving alerts from sensors

\- Logstash: Log processor enriching and forwarding data

\- Elasticsearch: Distributed search and analytics engine

\- Kibana: Visualization and dashboard platform



**Sensor VM (Kali Linux)**

\- Snort Instance 1: Monitors host-only network segment (192.168.56.0/24)

\- Snort Instance 2: Monitors internal network segment (192.168.20.0/24)

\- Python Forwarders: Read Snort JSON alerts and stream to Kafka



**Traffic Generator VM (Kali Linux)**

\- Dedicated system for generating test traffic

\- Connected to seg-b internal network (192.168.20.0/24)

\- Equipped with penetration testing tools (nmap, hping3)



### Data Flow



```

1. Network Traffic → Snort Sensors

2. Snort Detection → JSON Alert Files

3. Python Forwarders → Kafka Topic (snort-alerts)

4. Kafka → Logstash Consumer

5. Logstash Processing → Alert Enrichment

6. Enriched Data → Elasticsearch Indices

7. Kibana Queries → Real-time Visualization

```

In short,

```

Network Traffic  

↓  

Snort Sensors  

↓  

JSON Alerts  

↓  

Python Forwarders  

↓  

Kafka (snort-alerts)  

↓  

Logstash  

↓  

Elasticsearch  

↓  

Kibana Dashboards  

```



**Architecture Diagram**: See `docs/project-architecture-diagram.png`



---



## Features



### Core Capabilities



- **Multi-Segment Monitoring**: Simultaneous monitoring of two distinct network segments

- **Real-Time Processing**: Sub-second alert processing and indexing

- **Scalable Architecture**: Kafka-based design allows easy addition of sensors

- **Alert Enrichment**: Automatic classification by severity, segment, and sensor

- **Comprehensive Visualization**: Seven distinct dashboard visualizations

- **Resource Efficient**: Total system footprint of 4.5GB RAM



### Detection Capabilities



\- ICMP-based reconnaissance detection

\- TCP SYN scan identification

\- SSH connection attempt monitoring

\- HTTP/HTTPS traffic analysis

\- Port scanning detection

\- Service enumeration alerts



---



## System Requirements



### Hardware Requirements



\- CPU: Intel Core i5 or equivalent (4+ cores recommended)

\- RAM: 16GB minimum

\- Storage: 60GB free disk space

\- Network: Multiple network adapters for VirtualBox



### Software Requirements



\- Windows 10 or Windows 11 (64-bit)

\- Windows Subsystem for Linux 2 (WSL2)

\- Ubuntu 22.04 LTS (WSL distribution)

\- Oracle VirtualBox 7.0 or later

\- Kali Linux (latest rolling release)



---



## Technology Stack



### Detection Layer



- **Snort 3.10.0.0**: Open-source network intrusion detection system

&nbsp; - Signature-based detection engine

&nbsp; - JSON alert output format

&nbsp; - Multiple instance support



### Streaming Layer



- **Apache Kafka 3.6.1**: Distributed event streaming platform

&nbsp; - Topic-based message organization

&nbsp; - Reliable message delivery

&nbsp; - Consumer group management

&nbsp; - Java version 11.0.29 used



### Processing Layer



- **Logstash 8.19.9**: Server-side data processing pipeline

&nbsp; - Kafka input plugin

&nbsp; - JSON parsing and filtering

&nbsp; - Elasticsearch output integration



### Storage Layer



- **Elasticsearch 8.19.9**: Distributed search and analytics engine

&nbsp; - Daily index rotation

&nbsp; - Full-text search capabilities

&nbsp; - RESTful API



### Visualization Layer



- **Kibana 8.19.9**: Data visualization and exploration platform

&nbsp; - Interactive dashboards

&nbsp; - Real-time data refresh

&nbsp; - Custom visualization builder



### Integration Layer



- **Python 3.10.12**: Custom alert forwarder implementation

&nbsp; - kafka-python library

&nbsp; - File tailing mechanism

&nbsp; - Metadata enrichment



---



## Project Structure



```

distributed-ids-project/

├── configs/                  # Configuration files for all components

│   ├── elasticsearch/

│   │   ├── elasticsearch.yml

│   │   └── jvm-custom.options

│   ├── kafka/

│   │   └── server.properties

│   ├── kibana/

│   │   └── kibana.yml

│   ├── logstash/

│   │   └── snort-pipeline.conf

│   └── snort/

│       ├── snort.lua

│       └── local.rules

├── dashboards/

│   └── exports/

│       └── export.ndjson     # Kibana dashboard export

├── docs/

│   ├── ARCHITECTURE.md       # Detailed architecture documentation

│   ├── SETUP.md              # Installation and setup guide

│   └── project-architecture-diagram.png

├── evidence/

│   ├── logs/

│   │   ├── alert-breakdown.json

│   │   ├── alert-timeline.json

│   │   ├── pipeline-summary.txt

│   │   ├── snort-alerts-raw.json

│   │   └── source-ip-analysis.json

│   ├── elasticsearch-indices.txt

│   ├── kafka-topic-info.txt

│   └── sample-alerts.json

├── screenshots/              # Documentation and validation screenshots

├── scripts/

│   ├── snort\_to\_kafka.py     # Alert forwarder for eth0

│   ├── snort\_to\_kafka\_eth1.py # Alert forwarder for eth1

│   └── start-sensors.sh      # Sensor startup script

├── .gitignore

└── README.md

```



---



## Installation Guide



### Quick Start



For detailed installation instructions, refer to `docs/SETUP.md`. The basic steps are:



1. **Prepare WSL Environment**

&nbsp;  - Enable WSL2 on Windows

&nbsp;  - Install Ubuntu 22.04 from Microsoft Store

&nbsp;  - Update system packages



2. **Install SIEM Components on WSL**

&nbsp;  - Install Java Development Kit

&nbsp;  - Install Elasticsearch, Logstash, and Kibana

&nbsp;  - Download and configure Apache Kafka

&nbsp;  - Configure all components with provided config files



3. **Create Virtual Machines**

&nbsp;  - Install VirtualBox

&nbsp;  - Create two Kali Linux VMs (Sensor and Traffic Generator)

&nbsp;  - Configure network adapters (Host-only and Internal Network)



4. **Configure Snort Sensors**

&nbsp;  - Install Snort 3 on Sensor VM

&nbsp;  - Apply configuration from `configs/snort/`

&nbsp;  - Deploy custom detection rules

&nbsp;  - Install Python forwarder scripts



5. **Verify Installation**

&nbsp;  - Start all services in correct order

&nbsp;  - Verify connectivity between components

&nbsp;  - Generate test traffic

&nbsp;  - Confirm alerts appear in Kibana



---



## Configuration



### Network Configuration



**WSL (SIEM Server)**

\- IP Address: 172.28.254.81

\- Kafka Listener: 0.0.0.0:9092

\- Elasticsearch: localhost:9200

\- Kibana: localhost:5601



**Sensor VM Network Interfaces**

\- eth0 (Host-only): 192.168.56.10

\- eth1 (Internal seg-b): 192.168.20.10

\- eth2 (NAT): DHCP



**Traffic Generator VM**

\- eth0 (Internal seg-b): 192.168.20.20



### Key Configuration Points



**Snort Configuration** (`configs/snort/snort.lua`)

\- HOME\_NET: Defines protected networks

\- Alert output: JSON format for easy parsing

\- Rule inclusion: Custom rules from local.rules



**Kafka Configuration** (`configs/kafka/server.properties`)

\- advertised.listeners: Must match WSL IP address

\- Topic configuration: snort-alerts topic

\- Log retention: Configured for demo purposes



**Logstash Pipeline** (`configs/logstash/snort-pipeline.conf`)

\- Input: Kafka consumer on snort-alerts topic

\- Filters: Severity classification based on alert type

\- Output: Elasticsearch with daily index rotation



**Elasticsearch Configuration** (`configs/elasticsearch/elasticsearch.yml`)

\- Cluster name: snort-ids-cluster

\- Memory allocation: 1GB heap (optimized for WSL)

\- Security: Disabled for demonstration purposes



---



## Usage



### Starting the System



**Step 1: Start SIEM Server (WSL)**



```bash

\# Navigate to Kafka directory

cd ~/kafka/kafka\_2.13-3.6.1



\# Start Zookeeper

./bin/zookeeper-server-start.sh -daemon config/zookeeper.properties

sleep 10



\# Start Kafka

./bin/kafka-server-start.sh -daemon config/server.properties

sleep 15



\# Start Elasticsearch

sudo systemctl start elasticsearch

sleep 30



\# Start Logstash

sudo systemctl start logstash

sleep 20



\# Start Kibana

sudo systemctl start kibana

sleep 30

```



**Step 2: Start Snort Sensors (Sensor VM)**



```bash

\# Execute startup script

./start-sensors.sh



\# Verify sensors running

ps aux | grep snort

```



**Step 3: Access Kibana Dashboard**



Open web browser and navigate to: `http://localhost:5601`



### Generating Test Traffic



**From Traffic Generator VM:**



```bash

\# ICMP testing

ping -c 50 192.168.20.10



\# Port scanning

nmap -sS 192.168.20.10



\# Service detection

nmap -sV -p 22,80,443 192.168.20.10

```



**From WSL:**



```bash

\# ICMP testing on host-only network

ping -c 50 192.168.56.10



\# Port scanning

nmap -sS 192.168.56.10

```



### Stopping the System



**Stop Sensors (Sensor VM):**

```bash

sudo pkill snort

sudo pkill -f snort\_to\_kafka

```



**Stop SIEM Services (WSL):**

```bash

cd ~/kafka/kafka\_2.13-3.6.1

./bin/kafka-server-stop.sh

./bin/zookeeper-server-stop.sh

sudo systemctl stop kibana logstash elasticsearch

```



---



## Testing and Validation



### Pipeline Validation



Each component of the data pipeline was independently validated:



**Stage 1: Snort Detection**

\- Verification: JSON alert files created in /var/log/snort/

\- Method: Monitored alert\_json.txt during traffic generation

\- Result: Real-time alert generation confirmed



**Stage 2: Kafka Message Streaming**

\- Verification: Kafka console consumer displayed incoming alerts

\- Method: Monitored snort-alerts topic

\- Result: Zero message loss during testing



**Stage 3: Logstash Processing**

\- Verification: Pipeline logs showed successful message processing

\- Method: Monitored /var/log/logstash/logstash-plain.log

\- Result: Alerts enriched with metadata fields



**Stage 4: Elasticsearch Indexing**

\- Verification: Indices created with correct naming convention

\- Method: Queried Elasticsearch REST API

\- Result: Real-time indexing confirmed



**Stage 5: Kibana Visualization**

\- Verification: Dashboard displayed real-time data

\- Method: Loaded pre-built dashboard

\- Result: All visualizations rendering correctly



### Performance Testing



- **Alert Processing Latency**: Average 450ms from detection to indexing

- **System Resource Usage**: 4.5GB RAM total across all components

- **Alert Throughput**: Sustained 100+ alerts per minute

- **Data Retention**: Daily indices with configurable retention period



---



## Dashboard and Visualization



The Kibana dashboard provides comprehensive visibility into detected threats through seven key visualizations:



### Visualization Components



1. **Alert Timeline**

&nbsp;  - Type: Line chart

&nbsp;  - Purpose: Temporal distribution of alerts

&nbsp;  - Insight: Identifies attack patterns and peak activity periods



2. **Network Segment Distribution**

&nbsp;  - Type: Pie chart

&nbsp;  - Purpose: Alert distribution across monitored segments

&nbsp;  - Insight: Reveals which network segment experiences more threats



3. **Top Packet Lengths**

&nbsp;  - Type: Horizontal bar chart

&nbsp;  - Purpose: Most frequent alert categories

&nbsp;  - Insight: Identifies primary attack vectors



4. **Source IP Analysis**

&nbsp;  - Type: Data table

&nbsp;  - Purpose: Top attacking source addresses

&nbsp;  - Insight: Helps identify repeat offenders



5. **Severity Breakdown**

&nbsp;  - Type: Pie chart

&nbsp;  - Purpose: Distribution by severity level (high/medium/low)

&nbsp;  - Insight: Prioritization for security response



6. **Protocol Distribution**

&nbsp;  - Type: Pie chart

&nbsp;  - Purpose: Traffic breakdown by protocol

&nbsp;  - Insight: Understanding attack methodology



7. **Sensor Activity**

&nbsp;  - Type: Bar chart

&nbsp;  - Purpose: Alert count per sensor

&nbsp;  - Insight: Validates both sensors are operational



### Dashboard Access



The complete dashboard configuration can be imported from `dashboards/exports/export.ndjson`



---



## Results



### Alert Statistics



**Total Alerts Generated**: ~1500



**Alert Type Distribution**:

\- ICMP Ping Detection: 26.96% 

\- TCP Detection: 73.04% 



**Network Segment Distribution**:

\- Host-only Network (eth0): 95.87% 

\- Internal seg-b Network (eth1): 4.13% 



**Severity Classification**:

\- Low Severity: 45% (primarily ICMP)

\- Medium Severity: 40% (SSH, HTTP)

\- High Severity: 15% (port scans)



### Performance Metrics



\- **Average Processing Time**: 450ms per alert

\- **Kafka Message Lag**: 0 messages (real-time processing)

\- **Elasticsearch Query Response**: < 100ms average

\- **System Uptime**: Stable over 4-day testing period

\- **Memory Footprint**: 4.5GB total (50% reduction vs traditional dual-VM approach)



### Resource Efficiency Comparison



| Architecture | RAM Usage | Components |

|--------------|-----------|------------|

| Traditional (2 VMs) | ~10GB | Sensor VM (8GB) + SIEM VM (2GB) |

| This Implementation | ~4.5GB | WSL + Sensor VM + Generator VM |

| \*\*Savings\*\* | \*\*55%\*\* | Hybrid WSL approach |



---



## Challenges and Solutions



### Challenge 1: WSL to Virtual Machine Connectivity



**Problem**: Initial configuration had Kafka listening on localhost, preventing Kali VM from connecting.



**Solution**: Modified Kafka configuration to bind to 0.0.0.0 while advertising the specific WSL IP address (172.28.254.81). Added Windows Firewall rule to allow inbound connections on port 9092.



**Lesson Learned**: WSL networking requires explicit IP binding and firewall configuration for cross-VM communication.



### Challenge 2: Localhost Traffic Not Visible to Snort



**Problem**: Pinging the VM's own IP address from within the same VM did not generate alerts because traffic remained in the kernel.



**Solution**: Implemented dedicated Traffic Generator VM to ensure packets traverse the actual network interface where Snort operates in promiscuous mode.



**Lesson Learned**: Network monitoring requires traffic to physically cross the monitored interface; simulated traffic must originate from external sources.



### Challenge 3: Elasticsearch Memory Constraints



**Problem**: Default Elasticsearch configuration consumed excessive memory on WSL, causing system instability.



**Solution**: Created custom JVM options file limiting heap size to 1GB. Configured Elasticsearch for single-node operation to eliminate cluster coordination overhead.



**Lesson Learned**: Production defaults must be adjusted for resource-constrained demonstration environments.



### Challenge 4: Snort Configuration Complexity



**Problem**: Snort 3's Lua-based configuration differed significantly from previous versions, and default configurations included numerous unnecessary modules.



**Solution**: Started with distribution default configuration and selectively modified only essential parameters (HOME\_NET, alert output, rule inclusion). Disabled unused inspection modules.



**Lesson Learned**: When learning new software versions, modify existing working configurations rather than creating from scratch.



---



## Troubleshooting



### Common Issues



**1. Kafka Connection Refused**

```bash

\# Check Kafka is running

jps | grep Kafka



\# Check firewall

sudo ufw allow 9092

```



**2. No Data in Kibana**

```bash

\# Verify Elasticsearch has data

curl localhost:9200/snort-alerts-\*/\_count



\# Check time range in Kibana

```



**3. Snort Not Detecting Traffic**

```bash

\# Enable promiscuous mode

sudo ip link set eth0 promisc on



\# Generate traffic from different machine (not localhost)

```



---



## Future Enhancements



### Security Improvements



\- Enable TLS encryption for Kafka connections

\- Implement Elasticsearch authentication and role-based access control

\- Add firewall rules restricting management interface access

\- Deploy certificate-based authentication between components



### Scalability Enhancements



\- Implement Kafka cluster with multiple brokers for high availability

\- Deploy Elasticsearch cluster across multiple nodes

\- Add load balancing for multiple Snort sensors

\- Implement automated sensor registration and discovery



### Advanced Analytics



\- Integrate GeoIP database for source location enrichment

\- Implement machine learning models for anomaly detection

\- Add automated correlation of related alerts

\- Deploy threat intelligence feed integration



### Operational Features



\- Configure email alerting for high-severity detections

\- Implement Slack/Teams integration for alert notifications

\- Add PagerDuty integration for incident escalation

\- Create automated response playbooks



### Monitoring and Observability



\- Deploy Prometheus metrics collection

\- Add Grafana dashboards for system health monitoring

\- Implement log aggregation for all components

\- Create automated health check scripts



---



## Contributing



This project was developed as a cybersecurity internship demonstration project. While it is not actively maintained, suggestions and improvements are welcome.



To propose changes:

1. Fork the repository

2. Create a feature branch

3. Implement your changes with appropriate documentation

4. Submit a pull request with detailed description



---



## License



This project is provided as-is for educational and demonstration purposes. Individual components (Snort, Kafka, Elasticsearch, Logstash, Kibana) are subject to their respective open-source licenses.



---



## Acknowledgments



### Open Source Projects



\- **Snort Project**: For providing the industry-standard open-source IDS

\- **Apache Software Foundation**: For Apache Kafka

\- **Elastic**: For the ELK Stack (Elasticsearch, Logstash, Kibana)

\- **Kali Linux Team**: For comprehensive security testing distribution



### Documentation and Resources



\- Snort 3 Documentation: https://www.snort.org/snort3

\- Apache Kafka Documentation: https://kafka.apache.org/documentation/

\- Elastic Stack Guide: https://www.elastic.co/guide/

\- WSL Documentation: https://learn.microsoft.com/en-us/windows/wsl/



### Development Tools



\- VirtualBox for virtualization platform

\- Visual Studio Code for configuration editing

\- Git for version control



---



## Author



For questions or discussions about this implementation:



\- GitHub: @Samhithaa07(https://github.com/Samhithaa07)

\- Email: [j.samhitha.k@gmail.com](url)

\- Project Documentation: See `docs/` directory

\- Technical Details: See `docs/ARCHITECTURE.md`



---



**Project Completion Date**: 28th December 2024



**Documentation Version**: 1.0







