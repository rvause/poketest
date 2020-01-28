from unittest.mock import Mock

import pytest
import requests

from ..models import Pokemon, PokemonQuerySet
from .. import models

from . import sample_data


class TestPokemon:
    def test_str(self):
        obj = Pokemon(id=1, name="bulbasaur")
        assert f"{obj}" == "Bulbasaur #1"

    @pytest.mark.django_db
    def test_creation(self):
        obj = Pokemon.objects.create(
            id=760,
            name="bewear",
            height=21,
            weight=1350,
            types="normal, fighting",
        )

        assert obj.pk == 760
        assert obj.data == {}


@pytest.mark.django_db
class TestPokemonQuerySetWithDB:
    def test_get_by_id_found(self):
        obj = Pokemon.objects.create(
            id=760,
            name="bewear",
            height=21,
            weight=1350,
            types="normal, fighting",
        )
        result = Pokemon.objects.get_by_id(760)
        assert result == obj

    def test_get_by_id_api_found(self, monkeypatch):
        monkeypatch.setattr(
            models,
            "fetch_pokemon_data",
            Mock(return_value=sample_data.as_data),
        )
        result = Pokemon.objects.get_by_id(760)
        models.fetch_pokemon_data.assert_called_once_with(760)
        assert isinstance(result, Pokemon)
        assert result.pk == 760

    def test_get_by_id_not_found(self, monkeypatch):
        monkeypatch.setattr(
            models,
            "fetch_pokemon_data",
            Mock(side_effect=requests.exceptions.HTTPError),
        )
        with pytest.raises(Pokemon.DoesNotExist):
            Pokemon.objects.get_by_id(760)


class TestPokemonQuerySet:
    def test_get_by_id_found(self, monkeypatch):
        monkeypatch.setattr(PokemonQuerySet, "get", Mock(return_value="from_db"))
        assert Pokemon.objects.get_by_id(760) == "from_db"

    def test_get_by_id_api_found(self, monkeypatch):
        monkeypatch.setattr(
            PokemonQuerySet,
            "get",
            Mock(side_effect=Pokemon.DoesNotExist),
        )
        monkeypatch.setattr(
            models,
            "fetch_pokemon_data",
            Mock(return_value=sample_data.as_data),
        )
        monkeypatch.setattr(
            PokemonQuerySet,
            "_create_from_data",
            Mock(return_value="from_data"),
        )
        assert Pokemon.objects.get_by_id(760) == "from_data"

    def test_get_by_id_not_found(self, monkeypatch):
        monkeypatch.setattr(
            PokemonQuerySet,
            "get",
            Mock(side_effect=Pokemon.DoesNotExist),
        )
        monkeypatch.setattr(
            models,
            "fetch_pokemon_data",
            Mock(side_effect=requests.exceptions.HTTPError),
        )
        with pytest.raises(Pokemon.DoesNotExist):
            Pokemon.objects.get_by_id(760)

    def test_create_from_data(self, monkeypatch):
        monkeypatch.setattr(PokemonQuerySet, "create", Mock(return_value="created"))
        qs = PokemonQuerySet(Pokemon)
        assert qs._create_from_data(sample_data.as_data) == "created"
        PokemonQuerySet.create.assert_called_once_with(
            id=sample_data.as_data["id"],
            name=sample_data.as_data["name"],
            height=sample_data.as_data["height"],
            weight=sample_data.as_data["weight"],
            types="normal, fighting",
            image_url=sample_data.as_data["sprites"]["front_default"],
            data=sample_data.as_data,
        )
