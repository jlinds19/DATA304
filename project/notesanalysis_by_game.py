import json
import argparse
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict

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
by_game = defaultdict(list)

for entry in data:
    title = entry.get("title", "Unknown")
    notes = entry.get("responses", {}).get("notes", {})
    for note in notes.values():
        if isinstance(note, str):
            tokens = word_tokenize(note.lower())
            filtered = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
            by_game[title].extend(filtered)
# --------------------
# Frequency Analysis
# --------------------
# Print top words per game
for game, tokens in by_game.items():
    print(game, Counter(tokens).most_common(5))

