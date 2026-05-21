"""Kafka worker — consumes nl2sql.requests, publishes nl2sql.responses."""

import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

logger = logging.getLogger(__name__)

_consumer_task: asyncio.Task | None = None


async def _process(msg_value: dict, producer: AIOKafkaProducer) -> None:
    from services.nl2sql_service import nl2sql_service

    correlation_id = msg_value.get("correlation_id")
    action = msg_value.get("action", "generate")

    try:
        if action == "explain":
            sql_query = msg_value.get("sql_query", "")
            explanation = await asyncio.to_thread(nl2sql_service.explain_sql, sql_query)
            response = {"correlation_id": correlation_id, "success": True, "explanation": explanation}
        else:
            query = msg_value.get("query", "")
            result = await asyncio.to_thread(nl2sql_service.generate_sql, query)
            response = {
                "correlation_id": correlation_id,
                "success": result.success,
                "sql_query": result.sql_query,
                "explanation": result.explanation,
                "selected_tables": result.selected_tables,
                "intermediate_steps": [
                    {
                        "agent": s["agent"],
                        "input_summary": s["input_summary"],
                        "output_summary": s["output_summary"],
                        "raw_output": s.get("raw_output"),
                    }
                    for s in result.intermediate_steps
                ],
                "error": result.error,
            }
    except Exception as e:
        logger.error(f"[Kafka Worker] Processing error: {e}")
        response = {"correlation_id": correlation_id, "success": False, "error": str(e)}

    await producer.send_and_wait(
        "nl2sql.responses",
        value=json.dumps(response, default=str).encode("utf-8"),
    )
    logger.debug(f"[Kafka Worker] → nl2sql.responses [{correlation_id[:8] if correlation_id else '?'}]")


async def _worker_loop(bootstrap_servers: str) -> None:
    max_retries = 10
    retry_interval = 5
    
    consumer = None
    producer = None
    
    for i in range(max_retries):
        try:
            consumer = AIOKafkaConsumer(
                "nl2sql.requests",
                bootstrap_servers=bootstrap_servers,
                group_id="nl2sql-workers",
                auto_offset_reset="latest",
            )
            producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
            
            await consumer.start()
            await producer.start()
            logger.info("[Kafka Worker] NL2SQL worker started — listening on nl2sql.requests")
            break
        except Exception as e:
            logger.warning(f"[Kafka Worker] Connection attempt {i+1}/{max_retries} failed: {e}")
            if consumer:
                await consumer.stop()
            if producer:
                await producer.stop()
            if i < max_retries - 1:
                await asyncio.sleep(retry_interval)
            else:
                logger.error(f"[Kafka Worker] Failed to connect after {max_retries} attempts.")
                return
    try:
        async for msg in consumer:
            value = json.loads(msg.value.decode("utf-8"))
            asyncio.create_task(_process(value, producer))
    except asyncio.CancelledError:
        pass
    finally:
        await consumer.stop()
        await producer.stop()


async def start_worker(bootstrap_servers: str) -> None:
    global _consumer_task
    _consumer_task = asyncio.create_task(_worker_loop(bootstrap_servers))


async def stop_worker() -> None:
    global _consumer_task
    if _consumer_task:
        _consumer_task.cancel()
        try:
            await _consumer_task
        except asyncio.CancelledError:
            pass
        _consumer_task = None
