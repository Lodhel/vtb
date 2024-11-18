from aiokafka import AIOKafkaConsumer
from loguru import logger

from backend.app.config import PRODUCE_TOPIC, KAFKA_BOOTSTRAP_SERVERS


class AIOWebConsumer(object):
    def __init__(self):

        self.__produce_topic: str = PRODUCE_TOPIC
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            self.__produce_topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
        )

    async def start(self) -> None:
        await self.__consumer.start()

    async def stop(self) -> None:
        await self.__consumer.stop()

    async def consumption(self) -> None:
        await self.start()
        try:
            async for msg in self.__consumer:
                data_log: dict = {
                    'topic': msg.topic,
                    'partition': msg.partition,
                    'offset': msg.offset,
                    'key': msg.key,
                    'value': msg.value,
                    'timestamp': msg.timestamp
                }
                logger.info(data_log)
        finally:
            await self.stop()
