from django.contrib import admin

from .models import CharacterClue, DescriptorFlavorText, OccupationFlavorText

# Register your models here.
admin.site.register(OccupationFlavorText)
admin.site.register(DescriptorFlavorText)
admin.site.register(CharacterClue)
