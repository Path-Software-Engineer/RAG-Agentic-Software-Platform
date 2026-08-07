from __future__ import annotations

import os
from pathlib import Path

import psycopg


def main() -> None:
    database_url = os.environ["DATABASE_URL"]
    migrations = sorted(Path("/app/migrations").glob("*.sql"))
    if not migrations:
        raise RuntimeError("No database migrations were packaged.")

    with psycopg.connect(database_url, autocommit=True) as connection:
        connection.execute("SELECT pg_advisory_lock(hashtext('sf05-aws-migrations'))")
        try:
            for migration in migrations:
                connection.execute(migration.read_text(encoding="utf-8"))
        finally:
            connection.execute(
                "SELECT pg_advisory_unlock(hashtext('sf05-aws-migrations'))"
            )

    print(f"Applied {len(migrations)} idempotent database migrations.")


if __name__ == "__main__":
    main()
