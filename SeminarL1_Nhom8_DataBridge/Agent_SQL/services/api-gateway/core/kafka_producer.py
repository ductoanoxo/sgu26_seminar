"""Kafka producer — publishes requests to downstream services."""

import asyncio
import json
import logging
from aiokafka import AIOKafkaProducer
from core.kafka_consumer import register_pending

logger = logging.getLogger(__name__)

_producer: AIOKafkaProducer | None = None


async def start_producer(bootstrap_servers: str) -> None:
    global _producer
    max_retries = 10
    retry_interval = 5
    
    for i in range(max_retries):
        try:
            _producer = AIOKafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
            )
            await _producer.start()
            logger.info(f"[Kafka] Producer connected → {bootstrap_servers}")
            return
        except Exception as e:
            logger.warning(f"[Kafka] Producer connection attempt {i+1}/{max_retries} failed: {e}")
            _producer = None
            if i < max_retries - 1:
                await asyncio.sleep(retry_interval)
    
    logger.error(f"[Kafka] Producer failed to connect after {max_retries} attempts.")


async def stop_producer() -> None:
    global _producer
    if _producer:
        await _producer.stop()
        _producer = None


async def request(topic: str, payload: dict, timeout: float = 60.0) -> dict:
    """Publish a request and wait for the correlated response."""
    if _producer is None:
        raise RuntimeError("Kafka producer is not available")

    correlation_id = payload["correlation_id"]
    loop = asyncio.get_running_loop()
    future: asyncio.Future = loop.create_future()
    register_pending(correlation_id, future)

    await _producer.send_and_wait(topic, value=payload)
    logger.debug(f"[Kafka] → {topic} [{correlation_id[:8]}]")

    try:
        return await asyncio.wait_for(future, timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"No response from {topic} within {timeout}s")
