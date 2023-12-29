import folium
import json


from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url),
        )
        # for pokemon_entity in pokemon['entities']:
        #     add_pokemon(
        #         folium_map, pokemon_entity['lat'],
        #         pokemon_entity['lon'],
        #         pokemon['img_url']
        #     )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.pokemon.image.url,
            'title_ru': pokemon.pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']

    # requested_pokemon = PokemonEntity.objects.filter(id=pokemon_id).first()
    requested_pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    # print("Evolve: ", requested_pokemon.prev_evolution.id)

    if not requested_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    requested_pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    for pokemon_entity in requested_pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url),
        )

    pokemon_view_information = {
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
        "description": requested_pokemon.description,
        "previous_evolution": {
            "pokemon_id": requested_pokemon.prev_evolution.id,
            "img_url": request.build_absolute_uri(requested_pokemon.prev_evolution.image.url),
            "title_ru": requested_pokemon.prev_evolution.title_ru,
        } if requested_pokemon.prev_evolution else None,
        "next_evolution": {
            "pokemon_id": requested_pokemon.next_evolution.id,
            "img_url": request.build_absolute_uri(requested_pokemon.next_evolution.image.url),
            "title_ru": requested_pokemon.next_evolution.title_ru,
        } if requested_pokemon.next_evolution else None,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_view_information,
    })
