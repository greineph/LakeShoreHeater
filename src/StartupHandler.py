import os
import json

class Data:
    path_import = ""
    path_export = ""
    path_log = ""

def load_settings():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "startup.json"))
    if not os.path.exists(path):
        return

    with open(path, "r") as file:
        s = "".join(file.readlines())
        settings = json.loads(s)

    Data.path_import = settings.get("path_import", "")
    Data.path_export = settings.get("path_export", "")
    Data.path_log = settings.get("path_log", "")



def save_settings():
    settings = {
        "path_import" : Data.path_import,
        "path_export" : Data.path_export,
        "path_log" : Data.path_log,
    }
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "startup.json"))
    with open(path, "w") as file:
        s = json.dumps(settings, indent=4)
        file.write(s)

def to_string():
    print("path import: " + Data.path_import)
    print("path export: " + Data.path_export)
    print("path log   : " + Data.path_log)

