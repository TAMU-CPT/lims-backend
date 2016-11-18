from django.contrib import admin
from .models import AnnotationRecord


class AnnotationRecordAdmin(admin.ModelAdmin):
    queryset = AnnotationRecord.objects.all()
    list_display = ('id', 'phage', 'chado_id', 'apollo_id')

admin.site.register(AnnotationRecord, AnnotationRecordAdmin)
