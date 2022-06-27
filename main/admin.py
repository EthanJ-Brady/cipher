from django.contrib import admin
from .models import Deck, Source, CodenameCard

# Register your models here.
admin.site.register(Deck)
admin.site.register(Source)
admin.site.register(CodenameCard)
