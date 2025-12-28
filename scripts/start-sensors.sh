#!/bin/bash
echo "Starting Snort Sensors..."

sudo mkdir -p /var/log/snort /var/log/snort_eth1
sudo chmod 777 /var/log/snort /var/log/snort_eth1

sudo snort -c /etc/snort/snort.lua -i eth0 -A alert_json -l /var/log/snort -D
sudo snort -c /etc/snort/snort.lua -i eth1 -A alert_json -l /var/log/snort_eth1 -D

sleep 3

sudo /usr/local/bin/snort_to_kafka.py &
sudo /usr/local/bin/snort_to_kafka_eth1.py &

echo "✅ All sensors started"
