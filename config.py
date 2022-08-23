import json
from os.path import join

_ROOT_PATH = "/home/sanctity/image_bot"

def config_as_dict():
    """
        Returns project config.json as a Python dict.
    """
    with open(join(_ROOT_PATH, "config.json"), "r") as config_file:
        return json.loads(config_file.read())

def write_config(dikt):
    """
        Writes `dikt` to the config file.
        This function performs no checks. Use with caution.
    """
    with open(join(_ROOT_PATH, "config.json"), "w") as config_file:
        config_file.write(json.dumps(dikt))

def discord_client_token():
    with open(join(_ROOT_PATH, "config.json"), "r") as config_file:
        return json.loads(config_file.read())["discord_client_token"]

def discord_channel_id():
    with open(join(_ROOT_PATH, "config.json"), "r") as config_file:
        return int(json.loads(config_file.read())["discord_channel_id"])