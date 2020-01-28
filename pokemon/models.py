from operator import itemgetter

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.query import QuerySet

import requests

from .utils import fetch_pokemon_data


class PokemonQuerySet(QuerySet):
    def get_by_id(self, id):
        try:
            return self.get(pk=id)
        except Pokemon.DoesNotExist:
            try:
                return self._create_from_data(fetch_pokemon_data(id))
            except requests.exceptions.HTTPError:
                raise Pokemon.DoesNotExist()

    def _create_from_data(self, data):
        return self.create(
            id=data["id"],
            name=data["name"],
            height=data["height"],
            weight=data["weight"],
            types=", ".join(t["type"]["name"] for t in sorted(data["types"], key=itemgetter("slot"))),
            image_url=data["sprites"]["front_default"],
            data=data,
        )


class Pokemon(models.Model):
    """
    Model to store details about a Pokemon for presentation along with the full
    payload for archiving.

    """
    name = models.CharField(max_length=255)
    height = models.IntegerField()
    weight = models.IntegerField()
    types = models.CharField(max_length=255)
    image_url = models.URLField(max_length=255)

    data = JSONField(default=dict)

    objects = PokemonQuerySet.as_manager()

    class Meta:
        ordering = ("id",)
        verbose_name_plural = "pokémon"

    def __str__(self):
        return f"{self.name.title()} #{self.pk}"
