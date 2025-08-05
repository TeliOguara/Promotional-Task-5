import json
import os


FILE = "applications.json"

def load_applications():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_applications(apps):
    with open(FILE, "w") as f:
        json.dump(apps, f, indent=4)
