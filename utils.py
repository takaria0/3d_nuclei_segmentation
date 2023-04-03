import json
import re


def read_commented_json(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    re_text = re.sub(r"/\*[\s\S]*?\*/|//.*", "", text)
    json_obj = json.loads(re_text)
    return json_obj
