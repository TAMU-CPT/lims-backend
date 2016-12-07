from django.contrib import admin
from .models import Storage, Assembly, \
    ExperimentalResult, SequencingRun, SampleType, Experiment, Phage, \
    PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, \
    EnvironmentalSample, Lysate, Bacteria, EnvironmentalSampleCollection


class StorageAdmin(admin.ModelAdmin):
    queryset = Storage.objects.all()
    list_display = ('id', 'room', 'type', 'name', 'shelf', 'box', 'tube',)

class AssemblyAdmin(admin.ModelAdmin):
    queryset = Assembly.objects.all()
    list_display = ('id', 'notes', 'sequencing_run_pool_item', 'galaxy_dataset', )

class ExperimentalResultAdmin(admin.ModelAdmin):
    queryset = ExperimentalResult.objects.all()
    list_display = ('id', 'date', 'experiment', 'run_by', 'result',)

class SequencingRunAdmin(admin.ModelAdmin):
    queryset = SequencingRun.objects.all()
    list_display = ('id', 'date', 'name')

class SampleTypeAdmin(admin.ModelAdmin):
    queryset = SampleType.objects.all()
    list_display = ('id', 'name', )

class ExperimentAdmin(admin.ModelAdmin):
    queryset = Experiment.objects.all()
    list_display = ('id', 'full_name', 'short_name', 'methods',)

class PhageAdmin(admin.ModelAdmin):
    queryset = Phage.objects.all()
    list_display = ('id', 'historical_names', 'primary_name', )

class PhageDNAPrepAdmin(admin.ModelAdmin):
    queryset = PhageDNAPrep.objects.all()
    list_display = ('id', 'morphology', 'lysate', 'storage', )

class SequencingRunPoolAdmin(admin.ModelAdmin):
    queryset = SequencingRunPool.objects.all()
    list_display = ('id', 'run', 'pool',)

class SequencingRunPoolItemAdmin(admin.ModelAdmin):
    queryset = SequencingRunPoolItem.objects.all()
    list_display = ('id', 'pool',)

class EnvironmentalSampleAdmin(admin.ModelAdmin):
    queryset = EnvironmentalSample.objects.all()
    list_display = ('id', 'description', 'storage', 'sample_type', 'collection', 'location',)

class LysateAdmin(admin.ModelAdmin):
    queryset = Lysate.objects.all()
    list_display = ('id', 'oldid', 'isolation', 'storage')

class BacteriaAdmin(admin.ModelAdmin):
    queryset = Bacteria.objects.all()
    list_display = ('id', 'strain', 'genus', 'species')

class EnvironmentalSampleCollectionAdmin(admin.ModelAdmin):
    queryset = EnvironmentalSampleCollection.objects.all()
    list_display = ('id',)

admin.site.register(Assembly, AssemblyAdmin)
admin.site.register(ExperimentalResult, ExperimentalResultAdmin)
admin.site.register(SequencingRun, SequencingRunAdmin)
admin.site.register(SampleType, SampleTypeAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Phage, PhageAdmin)
admin.site.register(PhageDNAPrep, PhageDNAPrepAdmin)
admin.site.register(SequencingRunPool, SequencingRunPoolAdmin)
admin.site.register(SequencingRunPoolItem, SequencingRunPoolItemAdmin)
admin.site.register(EnvironmentalSample, EnvironmentalSampleAdmin)
admin.site.register(Lysate, LysateAdmin)
admin.site.register(Bacteria, BacteriaAdmin)
admin.site.register(EnvironmentalSampleCollection, EnvironmentalSampleCollectionAdmin)
