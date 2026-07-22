# MySQL raw data load

This folder now includes a MySQL-ready schema and a loader for the project dataset in `data/Raw_Data.csv`.

## Files

- `schema.sql` creates the `landslide_analysis` database and the `raw_data` table
- `load_raw_data.py` creates the database/table if needed and loads the CSV in batches

## Setup

1. Copy `.env.example` to `.env`
2. Fill in your MySQL connection values
3. Install dependencies:

```powershell
.\.venv\Scripts\pip.exe install -r requirements.txt
```

4. Run the loader:

```powershell
.\.venv\Scripts\python.exe sql\load_raw_data.py
```

## Useful options

```powershell
.\.venv\Scripts\python.exe sql\load_raw_data.py --if-exists append
.\.venv\Scripts\python.exe sql\load_raw_data.py --batch-size 2000
.\.venv\Scripts\python.exe sql\load_raw_data.py --table raw_data
```

By default, the loader uses `MYSQL_IF_EXISTS=replace`, so rerunning it refreshes the table instead of duplicating rows.
