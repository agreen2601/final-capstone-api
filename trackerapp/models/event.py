from django.db import models
from django.urls import reverse


class Event(models.Model):

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("event")
        verbose_name_plural = ("events")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})
