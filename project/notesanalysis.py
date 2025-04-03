import json
import argparse
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict
from datetime import datetime

# Download required resources
nltk.download('punkt')
nltk.download('stopwords')

# --------------------
# Argument parsing
# --------------------
parser = argparse.ArgumentParser(description="Analyze notes from ProtonDB JSON reports.")
parser.add_argument("--debug", action="store_true", help="Run on a small subset of the data for debugging")
args = parser.parse_args()

# --------------------
# Load JSON
# --------------------
with open("reports_piiremoved.json", "r") as f:
    data = json.load(f)

# If in debug mode, only take the first 5 entries
if args.debug:
    print("[DEBUG MODE] Using first 5 entries only...")
    data = data[:5]

# --------------------
# Token extraction
# --------------------
all_tokens = []

monthly_tokens = defaultdict(list)
stop_words = set(stopwords.words('english'))

for entry in data:
    notes = entry.get("responses", {}).get("notes", {})
    timestamp = entry.get("timestamp", None)

    if not timestamp:
        continue  # skip if no timestamp

    # Convert timestamp to YYYY-MM 
    date = datetime.utcfromtimestamp(timestamp)
    month_str = date.strftime('%Y-%m')  # Or use '%Y-%m-%d' for daily granularity

    for key, note_text in notes.items():
        if isinstance(note_text, str):
            tokens = word_tokenize(note_text.lower())
            filtered = [t for t in tokens if t.isalpha() and t not in stop_words]
            monthly_tokens[month_str].extend(filtered)

# --------------------
# Frequency Analysis
# --------------------
for month, tokens in sorted(monthly_tokens.items()):
    print(f"\n {month}")
    print(Counter(tokens).most_common(10))

