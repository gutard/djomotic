from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator


class HexField(models.CharField):
    def __init__(self, length, **kwargs):
        self.length = length
        kwargs['max_length'] = length * 2
        kwargs.setdefault('validators', []).extend([
            MinLengthValidator(length * 2),
            MaxLengthValidator(length * 2),
            RegexValidator(r'^[0-9a-f]*$', "Seuls 0-9 et a-f sont autorisés"),
        ])
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        kwargs['length'] = self.length
        return name, path, args, kwargs


class Device(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    address = HexField(verbose_name="Adresse", length=2)
    mac = HexField(verbose_name="Adresse MAC", length=4, blank=True)

    def __str__(self):
        return f"{self.name} ({self.address})"

    class Meta:
        verbose_name = "Appareil"


class Attribute(models.Model):
    device = models.ForeignKey(Device, verbose_name="Appareil", on_delete=models.PROTECT)
    endpoint = HexField(verbose_name="Extrémité", length=1)
    cluster = HexField(verbose_name="Groupe", length=2)
    number = HexField(verbose_name="Numéro", length=2)
    name = models.CharField(verbose_name="Nom", max_length=100, blank=True)
    unit = models.CharField(verbose_name="Unité", max_length=100, blank=True)
    exponent = models.IntegerField(verbose_name="Exposant", default=0)

    def __str__(self):
        return f"{self.name} ({self.device.address}:{self.endpoint}:{self.cluster}:{self.number})"

    class Meta:
        verbose_name = "Attribut"


class Value(models.Model):
    attribute = models.ForeignKey(Attribute, verbose_name="Attribut", on_delete=models.PROTECT)
    timestamp = models.DateTimeField(verbose_name="Horodatage")
    value = models.IntegerField(verbose_name="Valeur")

    class Meta:
        verbose_name = "Valeur"
