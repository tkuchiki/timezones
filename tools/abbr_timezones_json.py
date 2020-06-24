import json
import sys

def abbreviations():
    data = {}
    abbrs = {}
    timezones_json = sys.argv[1]
    with open(timezones_json) as f:
        data = json.load(f)

    for k in data:
        short_generic = data[k]["short"]["generic"]
        short_standard = data[k]["short"]["standard"]
        short_daylight = data[k]["short"]["daylight"]

        standard_offset = data[k]["standard_offset"]
        daylight_offset = data[k]["daylight_offset"]

        noskip = True
        if short_generic != "" and short_standard != "" and short_generic == short_standard:
            if not short_standard in abbrs:
                abbrs[short_standard] = []

            abbrs[short_generic].append(k)
            noskip = False
        elif short_generic != "":
            if not short_generic in abbrs:
                abbrs[short_generic] = []

            abbrs[short_generic].append(k)

        if short_standard != "" and noskip:
            if not short_standard in abbrs:
                abbrs[short_standard] = []

            abbrs[short_standard].append(k)

        if short_daylight != "" and standard_offset != daylight_offset:
            if not short_daylight in abbrs:
                 abbrs[short_daylight] = []

            abbrs[short_daylight].append(k)

    for k in abbrs:
        abbrs[k] = sorted(list(set(abbrs[k])))

    print(json.dumps(abbrs))

if __name__ == "__main__":
    abbreviations()