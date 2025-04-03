import json
import sqlite3
from datetime import datetime
import time

start_time = time.time()

# Load JSON data
with open("reports_piiremoved.json", "r") as f:
    data = json.load(f)

# Connect to (or create) SQLite database
conn = sqlite3.connect("protondb_reports.sqlite")
cursor = conn.cursor()

# Create schema
cursor.executescript("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_id TEXT,
    title TEXT
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    timestamp INTEGER,
    date TEXT,
    verdict TEXT,
    launcher TEXT,
    proton_version TEXT,
    type TEXT,
    FOREIGN KEY (game_id) REFERENCES games(id)
);

CREATE TABLE IF NOT EXISTS notes (
    report_id INTEGER,
    notes_combined TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(id)
);
""")

# Helper function to create or get game ID
def get_or_create_game(app_id, title):
    cursor.execute("SELECT id FROM games WHERE app_id = ?", (app_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute("INSERT INTO games (app_id, title) VALUES (?, ?)", (app_id, title))
    return cursor.lastrowid

# Insert data into database
for entry in data:
    game_info = entry.get("steam", {})
    app_id = game_info.get("appId")
    title = entry.get("title", "Unknown")

    game_id = get_or_create_game(app_id, title)

    timestamp = entry.get("timestamp")
    if not timestamp:
        continue

    date_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

    responses = entry.get("responses", {})
    verdict = responses.get("verdict")
    launcher = responses.get("launcher")
    proton_version = responses.get("protonVersion")
    type_field = responses.get("type")

    cursor.execute("""
        INSERT INTO reports (game_id, timestamp, date, verdict, launcher, proton_version, type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (game_id, timestamp, date_str, verdict, launcher, proton_version, type_field))

    report_id = cursor.lastrowid

    notes = responses.get("notes", {})
    combined_notes = " ".join([v for v in notes.values() if isinstance(v, str)])
    cursor.execute("INSERT INTO notes (report_id, notes_combined) VALUES (?, ?)", (report_id, combined_notes))

# Commit and close
conn.commit()
conn.close()
end_time = time.time()
elapsed = end_time - start_time
print(f"Export complete in {elapsed:.2f} seconds")

print("Export complete: data saved to protondb_reports.sqlite")


