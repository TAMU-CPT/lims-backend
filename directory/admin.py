from django.contrib import admin
from .models import Organisation

class OrganisationAdmin(admin.ModelAdmin):
    queryset = Organisation.objects.all()
    list_display = ('id', 'phone_number', 'website', 'name', 'fax_number', 'emails', 'street_address',)

admin.site.register(Organisation, OrganisationAdmin)
