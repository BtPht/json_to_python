import json

from formaters import AttrsFormater
from json_parser import FullMapping

if __name__ == "__main__":
    with open("examples/example3.json") as f:
        parsed = FullMapping.parse(json.load(f))

    s = AttrsFormater().to_str(parsed)

    print(s)

    with open("generated.py", "w") as f:
        f.write(s)
