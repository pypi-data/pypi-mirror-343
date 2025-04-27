import importlib

def load_plugin(plugin_type, plugin_name):
    module_path = f"plugins.{plugin_type}.{plugin_name}"
    return importlib.import_module(module_path)

def run_pipeline(input_plugin_name, processor_plugin_name, output_plugin_name, config):
    input_plugin = load_plugin('inputs', input_plugin_name)
    processor_plugin = load_plugin('processors', processor_plugin_name)
    output_plugin = load_plugin('outputs', output_plugin_name)

    print("[*] Running input plugin...")
    raw_data = input_plugin.fetch(config.get('input', {}))

    print("[*] Running processor plugin...")
    processed_data = processor_plugin.process(raw_data, config.get('processor', {}))

    print("[*] Running output plugin...")
    output_plugin.output(processed_data, config.get('output', {}))
