import json
import os

def get_mock_response(path):
    json_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json')
    with open(os.path.join(json_dir, "{}.json".format(path))) as f:
        return json.load(f)
