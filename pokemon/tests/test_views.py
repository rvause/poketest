from unittest.mock import Mock

from django.http import Http404
from django.urls import reverse

import pytest

from ..models import Pokemon, PokemonQuerySet
from ..views import PokemonDetail


@pytest.mark.urls("pokemon.urls")
class TestViews:
    def test_get_index(self, client):
        response = client.get(reverse("index"))
        assert response.status_code == 200
        assert "pokemon/index.html" in response.template_name

    def test_get_detail(self, client, monkeypatch):
        obj = Pokemon(
            id=760,
            name="bewear",
            height=21,
            weight=1350,
            types="normal, fighting",
            image_url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/760.png",
        )
        monkeypatch.setattr(PokemonQuerySet, "get_by_id", Mock(return_value=obj))
        response = client.get(reverse("detail", args=(760,)))
        assert response.status_code == 200
        assert "pokemon/pokemon_detail.html" in response.template_name
        assert f"<title>{obj}</title>" in response.content.decode()

    def test_get_detail_not_found(self, client, monkeypatch):
        monkeypatch.setattr(PokemonQuerySet, "get_by_id", Mock(side_effect=Pokemon.DoesNotExist))
        response = client.get(reverse("detail", args=(760,)))
        assert response.status_code == 404


class TestPokemonDetail:
    def test_get_object_found(self, monkeypatch):
        monkeypatch.setattr(PokemonQuerySet, "get_by_id", Mock(return_value="found"))

        view = PokemonDetail(kwargs={"pk": 760})
        assert view.get_object() == "found"
        PokemonQuerySet.get_by_id.assert_called_once_with(760)

    def test_get_object_not_found(self, monkeypatch):
        monkeypatch.setattr(PokemonQuerySet, "get_by_id", Mock(side_effect=Pokemon.DoesNotExist))
        with pytest.raises(Http404):
            view = PokemonDetail(kwargs={"pk": 760})
            view.get_object()
