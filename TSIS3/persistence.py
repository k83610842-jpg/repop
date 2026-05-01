# persistence.py handles saving and loading data from files
import json, os

# here we load leaderboard from file
def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    return []

# here we save leaderboard to file
def save_leaderboard(data):
    with open("leaderboard.json", "w") as f:
        json.dump(data, f)

# here we load settings from file or use defaults
def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return {"sound": True, "car_color": "red", "difficulty": "normal"}

# here we save settings to file
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)