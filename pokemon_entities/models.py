from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.TextField(max_length=200)
    image = models.ImageField(upload_to='pokemon', null=True)

    def __str__(self):
        return f"{self.title}"

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    Lat = models.FloatField()
    Lon = models.FloatField()