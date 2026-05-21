"""API Gateway — FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from core.kafka_producer import start_producer, stop_producer
from core.kafka_consumer import start_consumer, stop_consumer
from routers.gateway_router import router
from routers.import_proxy_router import router as import_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_producer(settings.KAFKA_BOOTSTRAP_SERVERS)
    await start_consumer(settings.KAFKA_BOOTSTRAP_SERVERS)
    yield
    await stop_consumer()
    await stop_producer()


app = FastAPI(
    title="NL2SQL API Gateway",
    description="Entry point for the NL2SQL system — orchestrates multi-agent pipeline and query execution",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=["Gateway"])
app.include_router(import_router)


@app.get("/")
async def root():
    return {"service": "api-gateway", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.SERVICE_HOST, port=settings.SERVICE_PORT, reload=settings.DEBUG)
