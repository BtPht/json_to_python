import json

from parser import FullMapping
from formaters import AttrsFormater


if __name__ == "__main__":
    with open("examples/example3.json") as f:
        parsed = FullMapping.parse(json.load(f))

    s = AttrsFormater().to_str(parsed)

    print(s)

    with open("generated.py", "w") as f:
        f.write(s)
