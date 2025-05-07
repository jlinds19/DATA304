import json

def explore_json(data, prefix=""):
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            explore_json(value, new_prefix)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_prefix = f"{prefix}[{i}]"
            explore_json(item, new_prefix)
    else:
        print(prefix)

with open("reports_piiremoved.json") as f:
    data = json.load(f)

# If it's a list of records, just sample the first
explore_json(data[0])
