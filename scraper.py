import os
import zipfile
import sqlite3
from bs4 import BeautifulSoup

def main():
    # Path to the ZIP file containing HTML submissions
    zip_file = "downloaded_class_submissions.zip"
    
    # Directory where the ZIP will be extracted
    extract_dir = "extracted_html"
    
    # SQLite database file
    db_file = "parsed_bios.sqlite"

    # 1) Unzip the submissions
    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(extract_dir)

    # 2) Set up the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    create_tables(cursor)

    # 3) Recursively parse each HTML file in the extracted folder and store in DB
    for root, dirs, files in os.walk(extract_dir):
        for filename in files:
            if filename.endswith(".html"):
                file_path = os.path.join(root, filename)
                name, favorites_list = parse_html(file_path)
                insert_data(cursor, name, favorites_list)

    conn.commit()
    conn.close()

    print("All HTML files processed and data stored in", db_file)

def create_tables(cursor):
    """
    Creates the necessary tables if they don't already exist.
    """
    # Table for names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS names (
            name_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)
    
    # Table for favorites
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_id INTEGER,
            category TEXT,
            favorite TEXT,
            FOREIGN KEY(name_id) REFERENCES names(name_id)
        )
    """)

def parse_html(html_file):
    """
    Opens and parses an HTML file, extracting:
      - The person's name (from <h1>)
      - A list of (category, favorite) tuples (from the <table>)
    Returns (name, favorites_list).
    """
    # Open file in binary mode to let BeautifulSoup handle encoding
    with open(html_file, "rb") as f:
        data = f.read()

    soup = BeautifulSoup(data, "html.parser")

    # Extract the name
    name_tag = soup.find("h1")
    name = name_tag.get_text(strip=True) if name_tag else "Unknown"
    print("Parsed name:", name)  # Debug output

    # Extract table rows for favorites
    favorites_list = []
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")[1:]  # skip the header row
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2:
                category = cells[0].get_text(strip=True)
                favorite = cells[1].get_text(strip=True)
                favorites_list.append((category, favorite))
        print("Parsed favorites:", favorites_list)  # Debug output

    return name, favorites_list

def insert_data(cursor, name, favorites_list):
    """
    Inserts the parsed data into the 'names' and 'favorites' tables.
    """
    try:
        # Insert the person's name
        cursor.execute(
            "INSERT INTO names (name) VALUES (?)",
            (name,)
        )
        name_id = cursor.lastrowid

        # Insert each favorite entry
        for category, favorite in favorites_list:
            cursor.execute(
                "INSERT INTO favorites (name_id, category, favorite) VALUES (?, ?, ?)",
                (name_id, category, favorite)
            )
    except Exception as e:
        print(f"Error inserting data for {name}: {e}")

if __name__ == "__main__":
    main()
