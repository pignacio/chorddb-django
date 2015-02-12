from django.contrib import admin

from .models import Song, InstrumentModel

admin.site.register(Song, admin.ModelAdmin)
admin.site.register(InstrumentModel, admin.ModelAdmin)
