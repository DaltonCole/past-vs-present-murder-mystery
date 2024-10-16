from django.contrib import admin
from .models import OccupationFlavorText, DescriptorFlavorText, TextClue

# Register your models here.
admin.site.register(OccupationFlavorText)
admin.site.register(DescriptorFlavorText)
admin.site.register(TextClue)
