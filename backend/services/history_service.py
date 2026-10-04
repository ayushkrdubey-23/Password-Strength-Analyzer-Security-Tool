"""
Privacy-first password analysis history service.

Only non-sensitive analysis metadata is stored.

Never store:
- Submitted passwords
- Generated passwords
- Password hashes
- Matched dictionary words
"""

import sqlite3

from datetime import datetime, timezone
from pathlib import Path

from flask import current_app


CREATE_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    score INTEGER NOT NULL,
    strength TEXT NOT NULL,
    findings_count INTEGER NOT NULL,
    character_types_count INTEGER NOT NULL,
    analysis_completed INTEGER NOT NULL
)
"""


def _get_database_path():
    """Resolve the configured SQLite database path."""

    configured_path = Path(
        current_app.config.get(
            "DATABASE_PATH",
            "instance/analytics.db"
        )
    )

    if not configured_path.is_absolute():
        project_root = Path(__file__).resolve().parents[2]
        configured_path = project_root / configured_path

    return configured_path


def _get_connection():
    """Create a SQLite connection and initialize its table."""

    database_path = _get_database_path()

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        str(database_path),
        timeout=5
    )

    connection.row_factory = sqlite3.Row

    try:
        connection.execute(CREATE_HISTORY_TABLE)
        connection.commit()
    except Exception:
        connection.close()
        raise

    return connection


def save_analysis_metadata(metadata: dict) -> dict:
    """
    Save explicitly submitted, non-sensitive analysis metadata.

    The API layer validates the metadata before calling this service.
    """

    created_at = datetime.now(
        timezone.utc
    ).isoformat(timespec="seconds")

    connection = _get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO analysis_history (
                created_at,
                score,
                strength,
                findings_count,
                character_types_count,
                analysis_completed
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                metadata["score"],
                metadata["strength"],
                metadata["findings_count"],
                metadata["character_types_count"],
                int(metadata["analysis_completed"])
            )
        )

        connection.commit()

        return {
            "id": cursor.lastrowid,
            "created_at": created_at,
            **metadata
        }

    finally:
        connection.close()


def get_analysis_history() -> list:
    """Return the latest 100 metadata-only history records."""

    connection = _get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                created_at,
                score,
                strength,
                findings_count,
                character_types_count,
                analysis_completed
            FROM analysis_history
            ORDER BY id DESC
            LIMIT 100
            """
        ).fetchall()

        return [
            {
                "id": row["id"],
                "created_at": row["created_at"],
                "score": row["score"],
                "strength": row["strength"],
                "findings_count": row["findings_count"],
                "character_types_count": row["character_types_count"],
                "analysis_completed": bool(
                    row["analysis_completed"]
                )
            }
            for row in rows
        ]

    finally:
        connection.close()


def clear_analysis_history() -> int:
    """Delete all stored analysis metadata."""

    connection = _get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM analysis_history"
        )

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()