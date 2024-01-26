from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_superuser',)


admin.site.register(CustomUser, CustomUserAdmin)
