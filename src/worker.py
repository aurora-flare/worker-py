import asyncio
from typing import Iterable
from typing import TypedDict

import paho.mqtt.client as mqtt
import redis.asyncio as aredis

from src.config import Settings

client = mqtt.Client()
cfg = Settings()


class Message(TypedDict):
    topic: str
    data: Iterable[int]


async def process_message(message: Message):
    client.publish(message['topic'], bytes(message['data']))


async def consume_messages():
    redis = aredis.Redis(
        host=cfg.REDIS_HOST, port=cfg.REDIS_PORT, decode_responses=True
    )
    while True:
        queue, message = await redis.blpop(cfg.REDIS_QUEUE)
        if message:
            await process_message(message)


if __name__ == '__main__':
    client.username_pw_set(cfg.MQTT_LOGIN, cfg.MQTT_PASSWORD)
    client.on_connect = lambda *_: print('Connected')

    client.connect(cfg.MQTT_HOST, cfg.MQTT_PORT, 60)
    client.loop_start()

    asyncio.run(consume_messages())
