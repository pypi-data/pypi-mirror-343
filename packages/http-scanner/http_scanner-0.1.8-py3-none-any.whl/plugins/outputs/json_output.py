import json

def output(processed_data, settings):
    output_path = settings.get('path', 'output.json')
    with open(output_path, 'w') as f:
        json.dump(processed_data, f, indent=2)
