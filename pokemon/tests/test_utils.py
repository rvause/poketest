from unittest.mock import Mock

import requests

from ..utils import fetch_pokemon_data, get_types


def test_fetch_pokemon_data(monkeypatch):
    response = Mock()
    response.json = Mock(return_value="json")
    monkeypatch.setattr(requests, "get", Mock(return_value=response))
    assert fetch_pokemon_data(1) == "json"

    requests.get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/1/")
    response.raise_for_status.assert_called_once()


def test_get_types():
    types = [
        {
            "slot": 2,
            "type": {"name": "Slot 2"},
        },
        {
            "slot": 3,
            "type": {"name": "Slot 3"}
        },
        {
            "slot": 1,
            "type": {"name": "Slot 1"}
        },
    ]
    assert get_types(types) == "Slot 1, Slot 2, Slot 3"
