import json
from runner import Nucleus3DSegmentation
from utils import read_commented_json

if __name__ == "__main__":
    settings = read_commented_json("./settings.json")
    print(json.dumps(settings, indent=4))
    app = Nucleus3DSegmentation(settings=settings)
    app.run()
