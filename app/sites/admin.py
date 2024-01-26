from django.contrib import admin
from .models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('name', 'user', 'url', 'visiting_count', 'data_volume')
