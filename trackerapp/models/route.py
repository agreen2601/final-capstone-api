from django.db import models
from django.urls import reverse


class Route(models.Model):

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("route")
        verbose_name_plural = ("routes")

    def __str__(self):
        return f'{self.name} {self.color}'

    def get_absolute_url(self):
        return reverse("route_detail", kwargs={"pk": self.pk})
