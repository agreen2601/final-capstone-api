from django.db import models
from django.urls import reverse
from .route import Route


class Place (models.Model):

    name = models.CharField(max_length=50)
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("place")
        verbose_name_plural = ("places")

    def __str__(self):
        return f'{self.name} {self.route}'

    def get_absolute_url(self):
        return reverse("place_detail", kwargs={"pk": self.pk})
