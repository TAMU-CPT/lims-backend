from django.contrib import admin
from .models import App

class AppAdmin(admin.ModelAdmin):
    queryset = App.objects.all()
    list_display = ('name', 'url', 'description', 'enabled', 'priority', 'hidden', 'id', 'icon',)

admin.site.register(App, AppAdmin)
