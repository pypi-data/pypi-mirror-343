import asyncio

from typing import Callable

from aiokafka import AIOKafkaConsumer

from ..settings import KafkaSettings


class CtesiphonAIOKafkaService:
    def __init__(
        self,
        topics: list[str],
        settings: KafkaSettings,
        group: str,
        topics_handler: Callable,
        container: any,
    ):
        self.settings = settings
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.settings.bootstrap,
            group_id=group,
        )
        self.topics_handler = topics_handler
        self.container = container

    async def serve(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                await self.topics_handler(self.container, msg)
        finally:
            await self.consumer.stop()

    def run(self):
        asyncio.run(self.serve())
