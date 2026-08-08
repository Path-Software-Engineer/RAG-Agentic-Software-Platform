from __future__ import annotations

import os
import sys
from typing import Any
from urllib.parse import parse_qs, urlparse


def load_database_url(parameter_name: str, ssm_client: Any | None = None) -> str:
    if not parameter_name.startswith("/sf/05/"):
        raise RuntimeError(
            "The database parameter is outside the Project 05 namespace."
        )

    if ssm_client is None:
        import boto3

        ssm_client = boto3.client("ssm")

    response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    database_url = str(response["Parameter"]["Value"])
    parsed = urlparse(database_url)
    if parsed.scheme not in {"postgres", "postgresql"} or not parsed.hostname:
        raise RuntimeError("The database parameter is not a PostgreSQL URL.")
    if parse_qs(parsed.query).get("sslmode") != ["require"]:
        raise RuntimeError("The database parameter must enforce sslmode=require.")
    return database_url


def main() -> None:
    parameter_name = os.environ.get("DATABASE_URL_PARAMETER_NAME", "")
    if not parameter_name:
        raise RuntimeError("DATABASE_URL_PARAMETER_NAME is required.")
    sys.stdout.write(load_database_url(parameter_name))


if __name__ == "__main__":
    main()
