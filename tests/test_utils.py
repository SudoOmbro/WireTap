import json


def get_test_config() -> dict:
    with open("test_config.json", "r") as file:
        return json.load(file)
