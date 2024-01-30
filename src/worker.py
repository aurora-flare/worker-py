import asyncio
import json
import logging.config
from typing import Iterable
from typing import TypedDict

import paho.mqtt.client as mqtt
import redis.asyncio as aredis

from src.config import Settings

client = mqtt.Client()
cfg = Settings()
logging.config.fileConfig('../logging.ini')
logger = logging.getLogger(__name__)


class Message(TypedDict):
    topic: str
    data: Iterable[int]


async def process_message(message: Message):
    client.publish(message['topic'], bytes(message['data']))


async def consume_messages():
    redis = aredis.Redis(host=cfg.REDIS_HOST, port=cfg.REDIS_PORT)
    while True:
        queue, message = await redis.blpop(cfg.REDIS_QUEUE)
        if message:
            await process_message(json.loads(message))


if __name__ == '__main__':
    client.username_pw_set(cfg.MQTT_LOGIN, cfg.MQTT_PASS)
    client.on_connect = lambda *_: logger.info(
        f'Client {cfg.CLIENT_ID} connected {cfg.MQTT_HOST}'
    )
    client.ondisconnect = lambda *_: logger.info(
        f'Client {cfg.CLIENT_ID} disconnect {cfg.MQTT_HOST}'
    )
    client.on_connect_fail = lambda *_: logger.info(
        f'Client {cfg.CLIENT_ID} fail connect {cfg.MQTT_HOST}'
    )

    client.connect(cfg.MQTT_HOST, cfg.MQTT_PORT, 60)
    client.loop_start()

    asyncio.run(consume_messages())
