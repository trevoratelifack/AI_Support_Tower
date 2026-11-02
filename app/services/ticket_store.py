"""Small local SQLite store for customer submissions and their workflow results."""
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "tickets.sqlite3"


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def _connection():
    connection = _connect()
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def save_ticket(ticket: dict, workflow_result: dict) -> None:
    with _connection() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                description TEXT NOT NULL,
                received_at TEXT NOT NULL,
                workflow_result TEXT NOT NULL
            )"""
        )
        connection.execute(
            """INSERT OR REPLACE INTO tickets
               (ticket_id, customer_id, subject, description, received_at, workflow_result)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (ticket["ticket_id"], ticket["customer_id"], ticket["subject"], ticket["description"],
             datetime.now(timezone.utc).isoformat(), json.dumps(workflow_result)),
        )


def list_tickets() -> list[dict]:
    with _connection() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                description TEXT NOT NULL,
                received_at TEXT NOT NULL,
                workflow_result TEXT NOT NULL
            )"""
        )
        rows = connection.execute("SELECT * FROM tickets ORDER BY received_at DESC").fetchall()
    return [
        {**dict(row), "workflow_result": json.loads(row["workflow_result"])}
        for row in rows
    ]
