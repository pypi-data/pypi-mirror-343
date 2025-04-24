# urlify-simple

A simple Python package that makes URL shortening super easy using TinyURL's API under the hood.

## Installation

```bash
pip install urlify-simple
```

## Usage

```python
from urlify import shorten_url

# Shorten a URL
short_url = shorten_url('https://www.example.com/very/long/url')
print(short_url)  # Outputs: http://tinyurl.com/xxxxx
```

## Features

- Simple one-function interface
- Uses reliable TinyURL service
- No API key required
- Clean error handling

## Requirements

- Python 3.6+
- requests library (automatically installed with package)

## License

This project is licensed under the MIT License.
