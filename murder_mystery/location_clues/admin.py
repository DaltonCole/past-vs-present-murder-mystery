from django.contrib import admin

from .models import Location, LocationClue

# Register your models here.
admin.site.register(LocationClue)
admin.site.register(Location)
