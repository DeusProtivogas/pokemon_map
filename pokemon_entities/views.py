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
    current_time = localtime()
    pokemons = PokemonEntity.objects.filter(
        appeared_at__lt=current_time,
        disappeared_at__gt=current_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url),
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.pokemon.id,
            'img_url': pokemon.pokemon.image.url,
            'title_ru': pokemon.pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.filter(id=pokemon_id).first()

    if not requested_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    print(requested_pokemon.pokemon_entity.all())
    print("EVOLVE 1: ", requested_pokemon.prev_evolution)
    print("EVOLVE 2: ", requested_pokemon.evolution.first())
    for pokemon_entity in requested_pokemon.pokemon_entity.all():
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
            "img_url": request.build_absolute_uri(
                requested_pokemon.prev_evolution.image.url
            ),
            "title_ru": requested_pokemon.prev_evolution.title_ru,
        } if requested_pokemon.prev_evolution else None,
        "next_evolution": {
            "pokemon_id": requested_pokemon.evolution.first().id,
            "img_url": request.build_absolute_uri(
                requested_pokemon.evolution.first().image.url
            ),
            "title_ru": requested_pokemon.evolution.first().title_ru,
        } if requested_pokemon.evolution.first() else None,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_view_information,
    })
