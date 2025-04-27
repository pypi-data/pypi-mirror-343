import argparse
import yaml
from core.runner import run_pipeline

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="HTTP Scanner")
    parser.add_argument('--input', required=True, help='Input plugin name')
    parser.add_argument('--processor', required=True, help='Processor plugin name')
    parser.add_argument('--output', required=True, help='Output plugin name')
    parser.add_argument('--config', required=True, help='Path to config file')

    args = parser.parse_args()
    config = load_config(args.config)

    run_pipeline(args.input, args.processor, args.output, config)

if __name__ == "__main__":
    main()
