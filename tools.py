import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "troubleshooting_steps.json")


def load_data():
    with open(JSON_FILE, "r") as file:
        return json.load(file)


def get_troubleshooting_steps(issue_type: str):
    """
    MCP-style tool function.
    Retrieves deterministic troubleshooting steps from JSON.
    """
    data = load_data()
    return data.get(issue_type)


def get_available_issues():
    data = load_data()
    return list(data.keys())