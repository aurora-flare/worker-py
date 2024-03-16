import json
import logging.config
from typing import Iterable
from typing import TypedDict

import paho.mqtt.client as mqtt
import redis
from config import Settings

cfg = Settings()
logging.config.fileConfig('../logging.ini')
logger = logging.getLogger(__name__)


class Message(TypedDict):
    topic: str
    data: Iterable[int]


def send(message: Message, mqtt_client: mqtt.Client) -> None:
    """Send message to specific mqtt topic, through mqtt client"""

    mqtt_client.publish(message['topic'], bytes(message['data']))


def main(mqtt_client: mqtt.Client):
    """Main loop. Listen for messages from broker and send them to matrix"""

    queue = redis.Redis(host=cfg.REDIS_HOST, port=cfg.REDIS_PORT)
    while True:
        _, message = queue.blpop(cfg.REDIS_QUEUE)
        if message:
            send(json.loads(message), mqtt_client)


if __name__ == '__main__':
    client = mqtt.Client()

    client.username_pw_set(cfg.MQTT_LOGIN, cfg.MQTT_PASS)
    client.on_connect = lambda *_: logger.info(f'{cfg.CLIENT_ID} connected success')
    client.ondisconnect = lambda *_: logger.info(f'{cfg.CLIENT_ID} disconnect')
    client.on_connect_fail = lambda *_: logger.info(f'{cfg.CLIENT_ID} fail connect')

    client.connect(cfg.MQTT_HOST, cfg.MQTT_PORT)
    client.loop_start()
    main(client)
