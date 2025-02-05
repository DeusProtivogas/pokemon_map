from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=50,
        verbose_name="Имя (Русское)"
    )
    title_en = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Имя (Английское)"
    )
    title_jp = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Имя (Японское)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    image = models.ImageField(
        upload_to='pokemon',
        null=True,
        verbose_name="Картинка"
    )
    prev_evolution = models.ForeignKey(
        "Pokemon",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="next_evolutions",
        verbose_name="Из кого эволюционирует",
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name="Покемон",
        related_name="entities",
    )
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Появился")
    disappeared_at = models.DateTimeField(verbose_name="Исчезнет")
    level = models.IntegerField(verbose_name="Уровень")
    heath_points = models.IntegerField(verbose_name="Здоровье")
    attack = models.IntegerField(verbose_name="Атака")
    defence = models.IntegerField(verbose_name="Защита")
    stamina = models.IntegerField(verbose_name="Выносливость")

    def __str__(self):
        return f"{self.pokemon.title_ru} - {self.id}"
