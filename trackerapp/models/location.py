from django.db import models
from django.urls import reverse
from .route import Route


class Location (models.Model):

    name = models.CharField(max_length=50)
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("location")
        verbose_name_plural = ("locations")

    def __str__(self):
        return f'{self.name} {self.route}'

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})
