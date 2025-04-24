# Open Interest Max Pain Calculator

A Python package for calculating max pain from open interest data.

## Installation

```bash
pip install openinterest
```

## Usage

```python
from openinterest import calculate_max_pain

# Example data
data = [
    {"expiration": "2024-03-22", "strike": 90, "type": "call", "open_interest": 100},
    {"expiration": "2024-03-15", "strike": 90, "type": "call", "open_interest": 100},
    {"expiration": "2024-03-15", "strike": 90, "type": "put", "open_interest": 50},
    {"expiration": "2024-03-15", "strike": 100, "type": "call", "open_interest": 200},
    {"expiration": "2024-03-15", "strike": 100, "type": "put", "open_interest": 150},
    {"expiration": "2024-03-15", "strike": 110, "type": "call", "open_interest": 50},
    {"expiration": "2024-03-15", "strike": 110, "type": "put", "open_interest": 200},
    {"expiration": "2024-03-15", "strike": 120, "type": "call", "open_interest": 20},
    {"expiration": "2024-03-15", "strike": 120, "type": "put", "open_interest": 300},
    {"expiration": "2024-03-15", "strike": 130, "type": "call", "open_interest": 10},
    {"expiration": "2024-03-15", "strike": 130, "type": "put", "open_interest": 400},
]
# Calculate max pain
max_pain_price, pain_values = calculate_max_pain(data)

print(f"Max pain price: {max_pain_price}")
```

## Development

To set up the development environment:

```bash
git clone https://github.com/charlesverge/openinterest.git
cd openinterest
pip install -e .
```

## Testing

Run the tests with:

```bash
pytest
```

## License

MIT License
