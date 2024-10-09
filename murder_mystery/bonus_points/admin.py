from django.contrib import admin
from .models import BonusPoint, TeamToBonusPoint

# Register your models here.
admin.site.register(BonusPoint)
admin.site.register(TeamToBonusPoint)
