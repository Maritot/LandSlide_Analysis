from __future__ import annotations

import argparse
import csv
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Callable

import pymysql
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CSV_PATH = ROOT_DIR / "data" / "Raw_Data.csv"
VALID_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def clean_text(value: str) -> str | None:
    stripped = value.strip()
    return stripped or None


def parse_date(value: str):
    cleaned = clean_text(value)
    if cleaned is None:
        return None
    return datetime.strptime(cleaned, "%Y-%m-%d").date()


def parse_float(value: str) -> float | None:
    cleaned = clean_text(value)
    if cleaned is None:
        return None
    return float(cleaned)


def parse_int(value: str) -> int | None:
    cleaned = clean_text(value)
    if cleaned is None:
        return None
    return int(float(cleaned))


COLUMN_SPECS: list[tuple[str, str, Callable[[str], object]]] = [
    ("Event_ID", "VARCHAR(20) NULL", clean_text),
    ("Date", "DATE NULL", parse_date),
    ("State", "VARCHAR(100) NULL", clean_text),
    ("District", "VARCHAR(100) NULL", clean_text),
    ("Latitude", "DECIMAL(10,6) NULL", parse_float),
    ("Longitude", "DECIMAL(10,6) NULL", parse_float),
    ("Season", "VARCHAR(30) NULL", clean_text),
    ("Rainfall_mm", "DECIMAL(10,2) NULL", parse_float),
    ("Elevation_m", "DECIMAL(10,2) NULL", parse_float),
    ("Slope_Degree", "DECIMAL(10,2) NULL", parse_float),
    ("Soil_Type", "VARCHAR(50) NULL", clean_text),
    ("NDVI", "DECIMAL(10,3) NULL", parse_float),
    ("Temperature_C", "DECIMAL(6,2) NULL", parse_float),
    ("Humidity", "DECIMAL(6,2) NULL", parse_float),
    ("Distance_to_River_km", "DECIMAL(10,2) NULL", parse_float),
    ("Land_Use", "VARCHAR(50) NULL", clean_text),
    ("Historical_Landslide_Count", "INT NULL", parse_int),
    ("Landslide_Occurred", "VARCHAR(10) NULL", clean_text),
    ("Landslide_Risk", "VARCHAR(20) NULL", clean_text),
    ("Casualties", "INT NULL", parse_int),
    ("Injured", "INT NULL", parse_int),
    ("Missing_Persons", "INT NULL", parse_int),
    ("Families_Affected", "INT NULL", parse_int),
    ("Population_Affected", "INT NULL", parse_int),
    ("Houses_Damaged", "INT NULL", parse_int),
    ("Roads_Blocked_km", "DECIMAL(10,2) NULL", parse_float),
    ("Bridges_Damaged", "INT NULL", parse_int),
    ("Economic_Loss_INR", "DECIMAL(15,2) NULL", parse_float),
    ("Cropland_Damaged", "DECIMAL(12,2) NULL", parse_float),
    ("Livestock_Lost", "INT NULL", parse_int),
    ("Response_ID", "VARCHAR(20) NULL", clean_text),
    ("Response_Time_Min", "DECIMAL(10,2) NULL", parse_float),
    ("Rescue_Duration_Hours", "DECIMAL(10,2) NULL", parse_float),
    ("Human_Resources_Deployed", "INT NULL", parse_int),
    ("Rescue_Teams", "INT NULL", parse_int),
    ("NDRF_Teams", "INT NULL", parse_int),
    ("SDRF_Teams", "INT NULL", parse_int),
    ("Volunteers", "INT NULL", parse_int),
    ("Ambulances", "INT NULL", parse_int),
    ("Helicopters", "INT NULL", parse_int),
    ("Excavators", "INT NULL", parse_int),
    ("JCB_Machines", "INT NULL", parse_int),
    ("Cranes", "INT NULL", parse_int),
    ("Relief_Camps", "INT NULL", parse_int),
    ("Evacuated_People", "INT NULL", parse_int),
    ("Aid_Amount_INR", "DECIMAL(15,2) NULL", parse_float),
    ("Relief_Materials_Tons", "DECIMAL(10,2) NULL", parse_float),
    ("Compensation_Provided", "VARCHAR(10) NULL", clean_text),
    ("Recovery_Days", "INT NULL", parse_int),
    ("Power_Outage_Hours", "DECIMAL(10,2) NULL", parse_float),
    ("Water_Supply_Disrupted", "VARCHAR(10) NULL", clean_text),
    ("Communication_Disruption", "VARCHAR(10) NULL", clean_text),
]


def require_identifier(value: str, label: str) -> str:
    if not VALID_IDENTIFIER.match(value):
        raise ValueError(f"{label} must contain only letters, numbers, and underscores: {value}")
    return value


def build_create_table_sql(table_name: str) -> str:
    columns_sql = ",\n  ".join(f"`{name}` {sql_type}" for name, sql_type, _ in COLUMN_SPECS)
    return f"""
CREATE TABLE IF NOT EXISTS `{table_name}` (
  `raw_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  {columns_sql},
  `loaded_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`raw_id`),
  KEY `idx_{table_name}_event_id` (`Event_ID`),
  KEY `idx_{table_name}_response_id` (`Response_ID`),
  KEY `idx_{table_name}_date` (`Date`),
  KEY `idx_{table_name}_state_district` (`State`, `District`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""".strip()


def iter_rows(csv_path: Path):
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        expected_columns = [name for name, _, _ in COLUMN_SPECS]
        if reader.fieldnames != expected_columns:
            raise ValueError(
                "CSV header does not match expected raw dataset columns.\n"
                f"Expected: {expected_columns}\n"
                f"Found: {reader.fieldnames}"
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                yield tuple(parser(row[column_name]) for column_name, _, parser in COLUMN_SPECS)
            except Exception as exc:
                raise ValueError(f"Failed to parse CSV row {line_number}: {exc}") from exc


def chunked(iterable, size: int):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def load_env() -> None:
    load_dotenv(ROOT_DIR / ".env")


def parse_args() -> argparse.Namespace:
    load_env()
    parser = argparse.ArgumentParser(description="Load data/Raw_Data.csv into a MySQL raw_data table.")
    parser.add_argument("--host", default=os.getenv("MYSQL_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MYSQL_PORT", "3306")))
    parser.add_argument("--user", default=os.getenv("MYSQL_USER", "root"))
    parser.add_argument("--password", default=os.getenv("MYSQL_PASSWORD", ""))
    parser.add_argument("--database", default=os.getenv("MYSQL_DATABASE", "landslide_analysis"))
    parser.add_argument("--table", default=os.getenv("MYSQL_TABLE", "raw_data"))
    parser.add_argument("--charset", default=os.getenv("MYSQL_CHARSET", "utf8mb4"))
    parser.add_argument("--csv", default=os.getenv("RAW_DATA_CSV_PATH", str(DEFAULT_CSV_PATH)))
    parser.add_argument("--batch-size", type=int, default=int(os.getenv("MYSQL_BATCH_SIZE", "1000")))
    parser.add_argument(
        "--if-exists",
        choices=["replace", "append"],
        default=os.getenv("MYSQL_IF_EXISTS", "replace"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    database_name = require_identifier(args.database, "Database name")
    table_name = require_identifier(args.table, "Table name")
    csv_path = Path(args.csv).expanduser()
    if not csv_path.is_absolute():
        csv_path = (ROOT_DIR / csv_path).resolve()

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    if args.batch_size < 1:
        raise ValueError("Batch size must be at least 1.")

    connection = pymysql.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        charset=args.charset,
        autocommit=False,
    )

    column_names = [name for name, _, _ in COLUMN_SPECS]
    insert_columns = ", ".join(f"`{name}`" for name in column_names)
    placeholders = ", ".join(["%s"] * len(column_names))
    insert_sql = f"INSERT INTO `{table_name}` ({insert_columns}) VALUES ({placeholders})"

    total_rows = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            cursor.execute(f"USE `{database_name}`")
            cursor.execute(build_create_table_sql(table_name))
            if args.if_exists == "replace":
                cursor.execute(f"TRUNCATE TABLE `{table_name}`")

        for batch in chunked(iter_rows(csv_path), args.batch_size):
            with connection.cursor() as cursor:
                cursor.executemany(insert_sql, batch)
            connection.commit()
            total_rows += len(batch)
            print(f"Loaded {total_rows} rows into {database_name}.{table_name}")

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    print(f"Done. Loaded {total_rows} rows from {csv_path} into {database_name}.{table_name}")


if __name__ == "__main__":
    main()
