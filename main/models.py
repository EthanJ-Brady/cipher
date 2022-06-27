from tkinter import CASCADE
from django.db import models

# Create your models here.
class Deck(models.Model):
    deck_title = models.CharField(max_length=30)

    def __str__(self):
        return self.deck_title

class Source(models.Model):
    source_title = models.CharField(max_length=30)

    def __str__(self):
        return self.source_title

class CodenameCard(models.Model):
    card_title = models.CharField(max_length=30)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="Cards", null=True)
    source = models.ManyToManyField(Source, blank=True, related_name="Cards")

    def __str__(self):
        return self.card_title