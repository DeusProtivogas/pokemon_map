from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.TextField(max_length=200)
    image = models.ImageField(upload_to='pokemon', null=True)

    def __str__(self):
        return f"{self.title}"

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
    description = models.TextField(max_length=200, default="")