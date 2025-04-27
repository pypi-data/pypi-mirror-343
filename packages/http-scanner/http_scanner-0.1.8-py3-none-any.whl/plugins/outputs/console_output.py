import json

def output(processed_data, settings):
    for item in processed_data:
        print(json.dumps(item, indent=2))
