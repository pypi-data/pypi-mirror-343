# http-scanner

A modular, plugin-based scanning framework designed to fetch and process HTTP-accessible targets (websites, APIs, etc.).  
Built for extensibility, supporting multiple input types, processors, and output destinations.

## Quick Start

```bash
pip install -e .
http-scanner --input http_input --processor idea_extractor --output console_output --config config.yaml
```
