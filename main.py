
"""
Main program that reads sensors, saves to data.json, and publishes to MQTT.
"""
from __future__ import annotations
import time
import json
import argparse
from sensors import TemperatureSensor, HumiditySensor, GPSSensor
from mqtt_client import MQTTClient

TOPICS = {
    'temperature': 'iot/sensor/temperature',
    'humidity': 'iot/sensor/humidity',
    'gps': 'iot/sensor/gps'
}


def parse_args():
    parser = argparse.ArgumentParser(description='IoT Sensor Simulator (with JSON logging)')
    parser.add_argument('--host', default='localhost', help='MQTT broker host (default: localhost)')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port (default: 1883)')
    parser.add_argument('--interval', type=float, default=1.0, help='Publish interval in seconds (default: 1.0)')
    parser.add_argument('--temp-center', type=float, default=22.0, help='Temperature center value in C (default: 22.0)')
    parser.add_argument('--qos', type=int, default=0, choices=[0, 1, 2], help='MQTT QoS (default: 0)')
    parser.add_argument('--log-file', default='data.json', help='JSON log file path (default: data.json)')
    return parser.parse_args()


def main():
    args = parse_args()

    # Sensors
    temp = TemperatureSensor(center_c=args.temp_center)
    hum = HumiditySensor()
    gps = GPSSensor()

    # MQTT client
    mqttc = MQTTClient(host=args.host, port=args.port, qos=args.qos)
    mqttc.connect()

    # Open JSON log file (append mode) - one JSON object per line (NDJSON)
    log_file = open(args.log_file, "a", encoding="utf-8")

    try:
        while True:
            # 1) Read sensors
            temp_data = temp.read()
            hum_data = hum.read()
            gps_data = gps.read()

            # 2) Save to JSON file (NDJSON = one JSON object per line)
            log_file.write(json.dumps(temp_data) + "\n")
            log_file.write(json.dumps(hum_data) + "\n")
            log_file.write(json.dumps(gps_data) + "\n")
            log_file.flush()  # يضمن الكتابة الفورية على القرص

            # 3) Publish to MQTT
            mqttc.publish_json(TOPICS['temperature'], temp_data)
            mqttc.publish_json(TOPICS['humidity'], hum_data)
            mqttc.publish_json(TOPICS['gps'], gps_data)

            # 4) Wait
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print('Stopping simulator...')

    finally:
        # Close MQTT and file
        mqttc.disconnect()
        log_file.close()


if __name__ == '__main__':
    main()
