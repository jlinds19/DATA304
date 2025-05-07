import json

def collect_field_paths(obj, prefix="", fields=None):
    if fields is None:
        fields = set()

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            fields.add(new_prefix)
            collect_field_paths(value, new_prefix, fields)
    elif isinstance(obj, list):
        for item in obj:
            collect_field_paths(item, prefix, fields)

    return fields

# === Load JSON File ===
with open("reports_piiremoved.json", "r") as f:
    data = json.load(f)

# === Collect Unique Fields from All Records ===
field_paths = set()
for record in data:
    field_paths |= collect_field_paths(record)

# === Print Sorted Field Paths ===
for field in sorted(field_paths):
    print(field)

