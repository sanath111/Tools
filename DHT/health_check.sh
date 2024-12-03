#!/bin/bash

# Example health check script
services=("dht_sensor_blynk")

for service in "${services[@]}"; do
  if ! supervisorctl status $service | grep -q "RUNNING"; then
    supervisorctl restart $service > /dev/null 2>&1
  fi
done
