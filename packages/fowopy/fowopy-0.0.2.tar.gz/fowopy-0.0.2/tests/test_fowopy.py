import pytest
from fowopy import FOWOClient
from fowopy import FOWOConfig
from fowopy.schemas import League, Team, Player, Performance
from io import BytesIO
import pyarrow.parquet as pq
import pandas as pd


def test_health_check():
    """Tests health check from SDK"""
    config = FOWOConfig(fowo_base_url="http://0.0.0.0:8000", fowo_backoff=False)
    client = FOWOClient(config)
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API health check: Status successful"}


def test_list_leagues():
    """tests get leagues from SDK"""
    config = FOWOConfig(fowo_base_url="http://0.0.0.0:8000", backoff=False)
    client = FOWOClient(config)
    leagues_response = client.list_leagues()
    assert isinstance(leagues_response, list)
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 5


def test_bulk_player_file_parquet():
    """Tests bulk player download throgh SDK - Parquet"""
    config = FOWOConfig(fowo_base_url="http://0.0.0.0:8000", bulk_file_format="parquet")
    client = FOWOClient(config)
    player_file_parquet = client.get_bulk_player_file()
    player_table = pq.read_table(BytesIO(player_file_parquet))
    player_df = player_table.to_pandas()
    assert len(player_df) == 1018
