from django.contrib import admin
from directory.models import PersonTag, Organisation, Person

admin.site.register(PersonTag)
admin.site.register(Organisation)
admin.site.register(Person)
# Register your models here.
