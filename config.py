import json
from os.path import join

_ROOT_PATH = "/home/sanctity/chess_bot"

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

def register_player(name, user_id, nick=None):
    with open(join(_ROOT_PATH, "config.json"), "r") as config_file:
        current_json = json.loads(config_file.read())

    for dikt in current_json["known_players"]:
        if name == dikt["name"]:
            return
    else:
        # TODO make sure this doesn't break shit
        current_json["known_players"].append({"name": name, "user_id": user_id, "nick": nick if nick else ""})
        write_config(current_json)

def player_known(name):
    with open(join(_ROOT_PATH, "config.json"), "r") as config_file:
        current_json = json.loads(config_file.read())
        for dikt in current_json["known_players"]:
            if name == dikt["name"]:
                return True, dikt["user_id"]
        else:
            return False, None


