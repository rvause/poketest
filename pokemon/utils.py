from operator import itemgetter

import requests


POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"


def fetch_pokemon_data(id):
    url = f"{POKEAPI_BASE_URL}pokemon/{id}/"

    resp = requests.get(url)
    resp.raise_for_status()

    return resp.json()



def get_types(types):
    return ", ".join(
        t["type"]["name"] for t in sorted(types, key=itemgetter("slot"))
    )
