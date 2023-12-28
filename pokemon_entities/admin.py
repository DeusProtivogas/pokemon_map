from django.contrib import admin
from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity


class PokemonAdmin(admin.ModelAdmin):
    pass

class PokemonEntityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonEntity, PokemonEntityAdmin)
