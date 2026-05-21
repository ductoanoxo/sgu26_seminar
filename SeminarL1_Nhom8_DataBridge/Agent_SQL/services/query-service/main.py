"""Query Service — FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from core.kafka_worker import start_worker, stop_worker
from routers.query_router import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_worker(settings.KAFKA_BOOTSTRAP_SERVERS)
    yield
    await stop_worker()


app = FastAPI(
    title="NL2SQL Query Service",
    description="Executes validated SELECT queries against Supabase PostgreSQL",
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

app.include_router(router, tags=["Query"])


@app.get("/")
async def root():
    return {"service": "query-service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.SERVICE_HOST, port=settings.SERVICE_PORT, reload=settings.DEBUG)
