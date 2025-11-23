"""
Encapsulated MQTT client for publishing JSON messages.
"""
from __future__ import annotations
import json
import time
import logging
from typing import Optional
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, host: str = 'localhost', port: int = 1883,
                 client_id: Optional[str] = None, keepalive: int = 60, qos: int = 0):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.qos = qos
        self.client = mqtt.Client(client_id=client_id, clean_session=True)
        # Last Will message to indicate unexpected disconnect
        self.client.will_set('iot/status', payload=json.dumps({'status': 'offline'}), qos=0, retain=True)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_log = self._on_log
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
        self.log = logging.getLogger('MQTTClient')

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.log.info('Connected to MQTT broker %s:%s', self.host, self.port)
            # publish online status
            client.publish('iot/status', json.dumps({'status': 'online'}), qos=0, retain=True)
        else:
            self.log.error('MQTT connection failed with code %s', rc)

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.log.warning('Unexpected disconnection. rc=%s (reconnect loop will keep trying)', rc)
        else:
            self.log.info('Disconnected from broker')

    def _on_log(self, client, userdata, level, buf):
        # optional debug
        pass

    def connect(self):
        self.client.connect(self.host, self.port, self.keepalive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish_json(self, topic: str, payload: dict, retain: bool = False):
        msg = json.dumps(payload)
        result = self.client.publish(topic, msg, qos=self.qos, retain=retain)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            self.log.error('Publish failed: rc=%s', result.rc)
        else:
            self.log.info('Published to %s: %s', topic, msg)
