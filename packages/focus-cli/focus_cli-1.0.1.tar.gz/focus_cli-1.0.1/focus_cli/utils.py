import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump({}, f)
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def get_data_path(filename):
    return os.path.join(DATA_DIR, filename)
