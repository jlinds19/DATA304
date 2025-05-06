import json

def walk_json(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            walk_json(v, path)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            path = f"{prefix}[{i}]"
            walk_json(item, path)
    else:
        # Leaf node: print path, type, and a sample value
        print(f"{prefix} ({type(obj).__name__}): {repr(obj)}")
with open("reports_piiremoved.json") as f:
    data = json.load(f)

# Explore a sample if it's a list of reports
walk_json(data[0])
