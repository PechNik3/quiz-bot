import json
import os

STATS_PATH = os.path.join("data", "stats.json")


def load_stats():
    if not os.path.exists(STATS_PATH):
        return {}
    with open(STATS_PATH, 'r') as f:
        return json.load(f)


def save_stats(stats):
    os.makedirs(os.path.dirname(STATS_PATH), exist_ok=True)
    with open(STATS_PATH, 'w') as f:
        json.dump(stats, f, indent=2)
