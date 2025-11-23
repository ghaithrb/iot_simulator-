"""
Main program that reads sensors and publishes to MQTT.
"""
from __future__ import annotations
import time
import argparse
from sensors import TemperatureSensor, HumiditySensor, GPSSensor
from mqtt_client import MQTTClient

TOPICS = {
    'temperature': 'iot/sensor/temperature',
    'humidity': 'iot/sensor/humidity',
    'gps': 'iot/sensor/gps'
}


def parse_args():
    parser = argparse.ArgumentParser(description='IoT Sensor Simulator')
    parser.add_argument('--host', default='localhost', help='MQTT broker host (default: localhost)')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port (default: 1883)')
    parser.add_argument('--interval', type=float, default=1.0, help='Publish interval in seconds (default: 1.0)')
    parser.add_argument('--temp-center', type=float, default=22.0, help='Temperature center value in C (default: 22.0)')
    parser.add_argument('--qos', type=int, default=0, choices=[0,1,2], help='MQTT QoS (default: 0)')
    return parser.parse_args()


def main():
    args = parse_args()

    temp = TemperatureSensor(center_c=args.temp_center)
    hum = HumiditySensor()
    gps = GPSSensor()

    mqttc = MQTTClient(host=args.host, port=args.port, qos=args.qos)
    mqttc.connect()

    try:
        while True:
            mqttc.publish_json(TOPICS['temperature'], temp.read())
            mqttc.publish_json(TOPICS['humidity'], hum.read())
            mqttc.publish_json(TOPICS['gps'], gps.read())
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print('Stopping simulator...')
    finally:
        mqttc.disconnect()


if __name__ == '__main__':
    main()
