MQTT Brute Force Protector (Lightweight Log IDS)

A lightweight, production-ready Python script designed to perform real-time Log Parsing and automated incident detection on Eclipse Mosquitto brokers.

## 🔍 How it Works
The script acts as a localized Intrusion Detection System (IDS), tailing the `mosquitto.log` file generated inside your Docker volumes. It uses Regular Expressions (Regex) to parse authentication failures and triggers a critical security event when an IP exceeds the defined threshold.

## 🚀 Deployment
1. Ensure your Mosquitto container is logging to a persistent volume (e.g., `./mosquitto/log/mosquitto.log`).
2. Run the protector script alongside your infrastructure:
```bash
python mqtt_monitor.py
