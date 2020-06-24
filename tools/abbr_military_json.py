import json
import sys

def abbreviations():
    data = {}
    abbrs = {}
    military_timezones_json = sys.argv[1]
    with open(military_timezones_json) as f:
        data = json.load(f)

    for d in data:
        short = d["short"]["standard"]
        long = d["long"]["standard"]
        offset = d["standard_offset"]
        offset_hhmm = d["standard_offset_hhmm"]

        abbrs[short] = {
            "name": long,
            "offset": offset,
            "offset_hhmm": offset_hhmm,
        }

    print(json.dumps(abbrs))

if __name__ == "__main__":
    abbreviations()