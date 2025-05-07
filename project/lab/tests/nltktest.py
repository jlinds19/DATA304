import json
import nltk
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Load JSON data
with open("reports_piiremoved.json", "r") as f:
    data = json.load(f)

# Download once
nltk.download('punkt')
nltk.download('stopwords')

# Extract and process relevant text fields
all_tokens = []

for entry in data:
    notes = entry.get("notes", {})
    
    for note_text in notes.values():  # handles audioFaults, customizationsUsed, etc.
        if isinstance(note_text, str):
            tokens = word_tokenize(note_text.lower())
            filtered = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
            all_tokens.extend(filtered)

# Frequency analysis
freq = Counter(all_tokens)
print(freq.most_common(20))

