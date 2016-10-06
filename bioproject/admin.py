from django.contrib import admin

from bioproject.models import Bioproject, EditingRoleUser, EditingRoleGroup

admin.site.register(Bioproject)
admin.site.register(EditingRoleUser)
admin.site.register(EditingRoleGroup)
