import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from decimal import Decimal

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from psycopg.rows import dict_row

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("bankops")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bankops:bankops_dev_only@localhost:5432/bankops")


def connect():
    return psycopg.connect(DATABASE_URL, connect_timeout=3, row_factory=dict_row)


def initialize_database():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id BIGSERIAL PRIMARY KEY,
                account_id VARCHAR(30) NOT NULL,
                amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
                transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('deposit', 'withdrawal')),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
    logger.info("Database table ready")


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="BankOps Monitor - Training API", lifespan=lifespan)
Instrumentator().instrument(app).expose(app)


class TransactionInput(BaseModel):
    account_id: str = Field(min_length=1, max_length=30)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    transaction_type: str


@app.get("/")
def home():
    return {"service": "BankOps Monitor", "purpose": "fictional training environment"}


@app.get("/health")
def health():
    try:
        with connect() as connection:
            connection.execute("SELECT 1").fetchone()
        return {"status": "healthy", "database": "connected", "time": datetime.now(timezone.utc).isoformat()}
    except psycopg.Error:
        logger.exception("Health check failed: database unavailable")
        raise HTTPException(status_code=503, detail="Database unavailable")


@app.get("/transactions")
def list_transactions():
    try:
        with connect() as connection:
            records = connection.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 100").fetchall()
        return records
    except psycopg.Error:
        logger.exception("Could not list transactions")
        raise HTTPException(status_code=503, detail="Database unavailable")


@app.post("/transactions", status_code=201)
def create_transaction(transaction: TransactionInput):
    if transaction.transaction_type not in ("deposit", "withdrawal"):
        raise HTTPException(status_code=422, detail="Type must be deposit or withdrawal")
    try:
        with connect() as connection:
            record = connection.execute(
                """INSERT INTO transactions (account_id, amount, transaction_type)
                VALUES (%s, %s, %s) RETURNING *""",
                (transaction.account_id, transaction.amount, transaction.transaction_type),
            ).fetchone()
        logger.info("Created fictional transaction id=%s", record["id"])
        return record
    except psycopg.Error:
        logger.exception("Could not save transaction")
        raise HTTPException(status_code=503, detail="Database unavailable")


@app.get("/simulate/slow")
def slow_request():
    time.sleep(2)
    return {"message": "Simulated slow response completed", "delay_seconds": 2}
