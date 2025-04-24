# FOWOPY - Football World Python SDK

[![PyPI version](https://badge.fury.io/py/fowopy.svg)](https://badge.fury.io/py/fowopy)
[![Python Versions](https://img.shields.io/pypi/pyversions/fowopy.svg)](https://pypi.org/project/fowopy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for interacting with the Football World (FOWO) API. This library simplifies the process of accessing fantasy football data through the FOWO API.

## Features

- Simple, intuitive interface for accessing FOWO API endpoints
- Type-validated responses using Pydantic models
- Support for both CSV and Parquet bulk data downloads
- Automatic retries with exponential backoff
- Comprehensive test suite

## Installation

```bash
pip install fowopy
```

## Quick Start

```python
from fowopy import FOWOClient, FOWOConfig

# Create a configuration object
config = FOWOConfig(fowo_base_url="http://api.footballworld.com")

# Initialize the client
client = FOWOClient(config)

# Check API health
response = client.get_health_check()
print(response.json())  # {'message': 'API health check: Status successful'}

# Get a list of leagues
leagues = client.list_leagues()
for league in leagues:
    print(f"League: {league.league_name}, ID: {league.league_id}")
```

## Configuration Options

The `FOWOConfig` class accepts the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fowo_base_url` | str | http://0.0.0.0:8000 | Base URL for the FOWO API |
| `fowo_backoff` | bool | True | Enable exponential backoff for API calls |
| `fowo_backoff_max_time` | int | 30 | Maximum time in seconds to retry API calls |
| `fowo_bulk_file_format` | str | "csv" | Format for bulk file downloads ("csv" or "parquet") |

You can also set the base URL using the `FOWO_API_BASE_URL` environment variable.

## API Endpoints

### Health Check

```python
response = client.get_health_check()
```

### Leagues

```python
# List all leagues
leagues = client.list_leagues()

# List leagues with pagination
leagues = client.list_leagues(skip=10, limit=20)

# Filter leagues by name
leagues = client.list_leagues(league_name="Premier League")

# Get a specific league by ID
league = client.get_league_by_id(5002)
```

### Teams

```python
# List all teams
teams = client.list_teams()

# Filter teams by league
teams = client.list_teams(league_id=5002)

# Filter teams by name
teams = client.list_teams(team_name="Manchester United")
```

### Players

```python
# List all players
players = client.list_players()

# Filter players by name
players = client.list_players(first_name="Bryce", last_name="Young")

# Get a specific player by ID
player = client.get_player_by_id(2009)
```

### Performances

```python
# List all performances
performances = client.list_performances()

# Filter performances by date
performances = client.list_performances(minimum_last_changed_date="2024-04-01")
```

### Bulk Data Downloads

```python
# Download player data as CSV (default)
player_data = client.get_bulk_player_file()

# Download player data as Parquet
config = FOWOConfig(fowo_bulk_file_format="parquet")
client = FOWOClient(config)
player_data_parquet = client.get_bulk_player_file()

# Other bulk data endpoints
league_data = client.get_bulk_league_file()
performance_data = client.get_bulk_performance_file()
team_data = client.get_bulk_team_file()
team_player_data = client.get_bulk_team_player_file()
```

## Working with Bulk Data

### CSV Example

```python
import csv
from io import StringIO

# Get player data as CSV
player_file = client.get_bulk_player_file()

# Decode the byte content to a string
player_file_str = player_file.decode("utf-8-sig")
player_file_s = StringIO(player_file_str)

# Parse CSV
csv_reader = csv.reader(player_file_s)
rows = list(csv_reader)

# First row is the header
header = rows[0]
data = rows[1:]
```

### Parquet Example

```python
from io import BytesIO
import pyarrow.parquet as pq
import pandas as pd

# Configure client for Parquet
config = FOWOConfig(fowo_bulk_file_format="parquet")
client = FOWOClient(config)

# Get player data as Parquet
player_file_parquet = client.get_bulk_player_file()

# Load into pandas DataFrame
player_table = pq.read_table(BytesIO(player_file_parquet))
player_df = player_table.to_pandas()
```

## Error Handling

The SDK uses the `httpx` library for making HTTP requests. Errors are handled as follows:

- HTTP status errors (4xx, 5xx) raise `httpx.HTTPStatusError`
- Network/connection errors raise `httpx.RequestError`

When `fowo_backoff` is enabled (default), the SDK will automatically retry failed requests with exponential backoff.

```python
try:
    response = client.get_health_check()
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e.response.status_code} - {e.response.text}")
except httpx.RequestError as e:
    print(f"Request error: {str(e)}")
```

## Development

### Prerequisites

- Python 3.10+
- pip

### Setup

1. Clone the repository
2. Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
