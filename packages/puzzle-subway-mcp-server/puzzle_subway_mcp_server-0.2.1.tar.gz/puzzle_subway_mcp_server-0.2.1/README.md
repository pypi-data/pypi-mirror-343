# Puzzle Subway MCP Server

A FastMCP server for subway information in Seoul.

## Installation

```bash
pip install puzzle-subway-mcp-server
```

## Usage

```python
from puzzle_subway_mcp_server import get_subway_congestion

# Get congestion information for a station
congestion = get_subway_congestion("을지로입구")
print(congestion)
```

## Features

- Real-time subway congestion information
- Station-based search
- Line-based search

## License

MIT
