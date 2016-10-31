from django.contrib import admin
from .models import EditingRoleUser, EditingRoleGroup, Bioproject

class EditingRoleUserAdmin(admin.ModelAdmin):
    queryset = EditingRoleUser.objects.all()
    list_display = ('id', 'role', 'user', 'bioproject',)

class EditingRoleGroupAdmin(admin.ModelAdmin):
    queryset = EditingRoleGroup.objects.all()
    list_display = ('id', 'role', 'group', 'bioproject',)

class BioprojectAdmin(admin.ModelAdmin):
    queryset = Bioproject.objects.all()
    list_display = ('id', 'name', 'date', 'description',)

admin.site.register(EditingRoleUser, EditingRoleUserAdmin)
admin.site.register(EditingRoleGroup, EditingRoleGroupAdmin)
admin.site.register(Bioproject, BioprojectAdmin)
