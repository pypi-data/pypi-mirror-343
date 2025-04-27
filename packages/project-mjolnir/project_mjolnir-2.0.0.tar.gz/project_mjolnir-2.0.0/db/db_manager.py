import sqlite3
import os

class DBManager:

    def __init__(self, db_path="db/mjolnir.db"):
        self.db_path = db_path
        self.ensure_db_exists()

    def ensure_db_exists(self):
        if not os.path.exists(self.db_path):
            print("[!] Database not found. Run the database initialization script first.")
            raise SystemExit(1)

    def connect(self):
        return sqlite3.connect(self.db_path)

    def insert(self, table, records):
        if not records:
            return

        with self.connect() as conn:
            cursor = conn.cursor()

            # Assume all records are dicts with the same keys
            columns = list(records[0].keys())
            placeholders = ','.join(['?' for _ in columns])
            query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

            data = [tuple(record.get(col, None) for col in columns) for record in records]

            try:
                cursor.executemany(query, data)
                conn.commit()
                print(f"[+] Inserted {len(records)} records into {table}")
            except Exception as e:
                print(f"[!] Failed to insert records into {table}: {e}")
