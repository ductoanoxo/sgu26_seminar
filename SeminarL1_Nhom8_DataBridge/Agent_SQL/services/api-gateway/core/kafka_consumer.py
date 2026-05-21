"""Kafka response consumer — resolves pending request futures."""

import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer

logger = logging.getLogger(__name__)

_pending: dict[str, asyncio.Future] = {}
_consumer_task: asyncio.Task | None = None


def register_pending(correlation_id: str, future: asyncio.Future) -> None:
    _pending[correlation_id] = future


def _resolve(correlation_id: str, data: dict) -> None:
    future = _pending.pop(correlation_id, None)
    if future and not future.done():
        future.set_result(data)


async def _consume_loop(bootstrap_servers: str) -> None:
    max_retries = 10
    retry_interval = 5
    
    consumer = None
    for i in range(max_retries):
        try:
            consumer = AIOKafkaConsumer(
                "nl2sql.responses",
                "query.responses",
                bootstrap_servers=bootstrap_servers,
                group_id="api-gateway-responses",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="latest",
            )
            await consumer.start()
            logger.info("[Kafka] Response consumer started — listening on nl2sql.responses, query.responses")
            break
        except Exception as e:
            logger.warning(f"[Kafka] Consumer connection attempt {i+1}/{max_retries} failed: {e}")
            if consumer:
                await consumer.stop()
            if i < max_retries - 1:
                await asyncio.sleep(retry_interval)
            else:
                logger.error(f"[Kafka] Consumer failed to connect after {max_retries} attempts.")
                return
    try:
        async for msg in consumer:
            data = msg.value
            correlation_id = data.get("correlation_id")
            if correlation_id:
                _resolve(correlation_id, data)
    except asyncio.CancelledError:
        pass
    finally:
        await consumer.stop()


async def start_consumer(bootstrap_servers: str) -> None:
    global _consumer_task
    try:
        _consumer_task = asyncio.create_task(_consume_loop(bootstrap_servers))
    except Exception as e:
        logger.warning(f"[Kafka] Consumer failed to start: {e}")


async def stop_consumer() -> None:
    global _consumer_task
    if _consumer_task:
        _consumer_task.cancel()
        try:
            await _consumer_task
        except asyncio.CancelledError:
            pass
        _consumer_task = None
