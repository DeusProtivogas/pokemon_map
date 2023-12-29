from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title_ru = models.TextField(max_length=200)
    title_en = models.TextField(max_length=200)
    title_jp = models.TextField(max_length=200)
    description = models.TextField(max_length=200, default="")
    image = models.ImageField(upload_to='pokemon', null=True)
    prev_evolution = models.ForeignKey("Pokemon", null=True, blank=True, on_delete=models.SET_NULL,  related_name="evolves_from")
    next_evolution = models.ForeignKey("Pokemon", null=True, blank=True, on_delete=models.SET_NULL, related_name="evolves_into")

    def __str__(self):
        return f"{self.title_ru}"

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(default=1)
    heath_points = models.IntegerField(default=10)
    attack = models.IntegerField(default=5)
    defence = models.IntegerField(default=5)
    stamina = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.pokemon.title_ru} - {self.id}"