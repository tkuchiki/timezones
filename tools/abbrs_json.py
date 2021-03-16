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

        long_generic = data[k]["long"]["generic"]
        long_standard = data[k]["long"]["standard"]
        long_daylight = data[k]["long"]["daylight"]

        standard_offset = data[k]["standard_offset"]
        daylight_offset = data[k]["daylight_offset"]

        noskip = True
        if short_generic != "" and short_standard != "" and short_generic == short_standard and not long_generic == long_standard:
            if not short_standard in abbrs:
                abbrs[short_standard] = []

            names = [d.get('name') for d in abbrs[short_standard] if long_standard in d.get('name')]
            name = long_generic + "/" + long_standard
            if name not in names:
                abbrs[short_generic].append({
                    "name": name,
                    "offset": data[k]["standard_offset"],
                    "offset_hhmm": data[k]["standard_offset_hhmm"],
                    "is_dst": False,
                    "country_code": data[k]["country_code"],
                })
                noskip = False
        elif short_generic != "":
            if not short_generic in abbrs:
                abbrs[short_generic] = []

            names = [d.get('name') for d in abbrs[short_generic] if long_generic in d.get('name')]
            if long_generic not in names:
                abbrs[short_generic].append({
                    "name": long_generic,
                    "offset": data[k]["standard_offset"],
                    "offset_hhmm": data[k]["standard_offset_hhmm"],
                    "is_dst": False,
                    "country_code": data[k]["country_code"],
                })


        if short_standard != "" and noskip:
            if not short_standard in abbrs:
                abbrs[short_standard] = []

            names = [d.get('name') for d in abbrs[short_standard] if long_standard in d.get('name')]
            name = long_generic + "/" + long_standard
            if long_standard not in names and name not in names:
                abbrs[short_standard].append({
                    "name": long_standard,
                    "offset": data[k]["standard_offset"],
                    "offset_hhmm": data[k]["standard_offset_hhmm"],
                    "is_dst": False,
                    "country_code": data[k]["country_code"],
                })

        if short_daylight != "" and standard_offset != daylight_offset:
            if not short_daylight in abbrs:
                 abbrs[short_daylight] = []

            names = [d.get('name') for d in abbrs[short_daylight] if d.get('name')]
            if long_daylight not in names:
                abbrs[short_daylight].append({
                    "name": long_daylight,
                    "offset": data[k]["daylight_offset"],
                    "offset_hhmm": data[k]["daylight_offset_hhmm"],
                    "is_dst": True,
                    "country_code": data[k]["country_code"],
                })

        abbrs["GMT"][0]["country_code"] = ""
    
    additional_abbrs_json = sys.argv[2]
    with open(additional_abbrs_json) as f:
        data = json.load(f)

    abbrs.update(data)
    print(json.dumps(abbrs))

if __name__ == "__main__":
    abbreviations()
