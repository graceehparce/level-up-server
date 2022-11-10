from configparser import NoSectionError
from django.db import models
from django.contrib.auth.models import User


class EventGamer(models.Model):

    gamer = models.ForeignKey(
        "Gamer", on_delete=models.CASCADE, related_name='attending_gamer')
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name='event_attending')
