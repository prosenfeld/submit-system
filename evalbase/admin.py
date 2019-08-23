from django.contrib import admin
from .models import *

admin.site.register(UserProfile)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = [ 'passphrase' ]
