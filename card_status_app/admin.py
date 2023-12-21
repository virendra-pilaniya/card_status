from django.contrib import admin

from .models import Card, CardEvent

admin.site.register(Card)
admin.site.register(CardEvent)