from django.contrib import admin
from .models import PersonTag, Organisation

class PersonTagAdmin(admin.ModelAdmin):
    queryset = PersonTag.objects.all()
    list_display = ('id',)

class OrganisationAdmin(admin.ModelAdmin):
    queryset = Organisation.objects.all()
    list_display = ('phone_number', 'website', 'name', 'fax_number', 'id', 'emails', 'street_address',)

admin.site.register(PersonTag, PersonTagAdmin)
admin.site.register(Organisation, OrganisationAdmin)
