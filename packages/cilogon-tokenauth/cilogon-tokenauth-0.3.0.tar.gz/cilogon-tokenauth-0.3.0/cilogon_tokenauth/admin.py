from django.contrib import admin
from cilogon_tokenauth.models import *

# Register your models here.


class CachedToken_Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'scope', 'expires_at', 'last_introspection')
    list_display_links = ['id']
    ordering = ['user']
    search_fields = ['user']


admin.site.register(CachedToken, CachedToken_Admin)
