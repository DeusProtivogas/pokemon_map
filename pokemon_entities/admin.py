from django.contrib import admin
from pokemon_entities.models import Pokemon


class PokemonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pokemon, PokemonAdmin)
