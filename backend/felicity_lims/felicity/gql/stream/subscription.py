from typing import AsyncGenerator

import strawberry
import asyncio
import logging

from felicity.apps.core.channel import broadcast, Subscriber, BroadcastEvent
from felicity.apps.stream.models import ActivityStream
from felicity.gql.stream.types import ActivityStreamType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@strawberry.type
class StreamSubscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> int:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)

    @strawberry.subscription
    async def latest_stream(self) -> AsyncGenerator[ActivityStreamType, None]: # noqa
        subscriber: Subscriber
        async with broadcast.subscribe(channel="activities") as subscriber:
            logger.info("Subscribed")
            event: BroadcastEvent
            try:
                async for event in subscriber:
                    logger.info(event)
                    yield event.message
            finally:
                logger.info("Unsubscribed")

    @strawberry.subscription
    async def test_stream(self) -> AsyncGenerator[ActivityStreamType, None]: # noqa
        streams = await ActivityStream.all()
        for stream in streams:
            yield stream
            await asyncio.sleep(1)
