from django.contrib import admin
from .models import Box, StorageLocation, Assembly, TubeType, \
    ExperimentalResult, SequencingRun, Tube, SampleType, Experiment, Phage, \
    PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, ContainerType, \
    EnvironmentalSample, Lysate, Bacteria, EnvironmentalSampleCollection

class BoxAdmin(admin.ModelAdmin):
    queryset = Box.objects.all()
    list_display = ('id', 'name', 'location',)

class StorageLocationAdmin(admin.ModelAdmin):
    queryset = StorageLocation.objects.all()
    list_display = ('id', 'name', 'container_type', 'location',)

class AssemblyAdmin(admin.ModelAdmin):
    queryset = Assembly.objects.all()
    list_display = ('id', 'notes', 'sequencing_run_pool_item', 'galaxy_dataset', )

class TubeTypeAdmin(admin.ModelAdmin):
    queryset = TubeType.objects.all()
    list_display = ('id', 'name', )

class ExperimentalResultAdmin(admin.ModelAdmin):
    queryset = ExperimentalResult.objects.all()
    list_display = ('id', 'date', 'experiment', 'run_by', 'result',)

class SequencingRunAdmin(admin.ModelAdmin):
    queryset = SequencingRun.objects.all()
    list_display = ('id', 'methods', 'bioanalyzer_qc', 'date', 'galaxy_history', 'run_prep_spreadsheet', 'name',)

class TubeAdmin(admin.ModelAdmin):
    queryset = Tube.objects.all()
    list_display = ('id', 'box', 'type', 'name', )

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
    list_display = ('id', 'morphology', 'lysate', 'tube', )

class SequencingRunPoolAdmin(admin.ModelAdmin):
    queryset = SequencingRunPool.objects.all()
    list_display = ('id', 'run', 'pool',)

class SequencingRunPoolItemAdmin(admin.ModelAdmin):
    queryset = SequencingRunPoolItem.objects.all()
    list_display = ('id', 'pool',)

class ContainerTypeAdmin(admin.ModelAdmin):
    queryset = ContainerType.objects.all()
    list_display = ('id', 'name', )

class EnvironmentalSampleAdmin(admin.ModelAdmin):
    queryset = EnvironmentalSample.objects.all()
    list_display = ('id', 'description', 'tube', 'sample_type', 'collection', 'location',)

class LysateAdmin(admin.ModelAdmin):
    queryset = Lysate.objects.all()
    list_display = ('id', 'oldid', 'isolation', 'tube')

class BacteriaAdmin(admin.ModelAdmin):
    queryset = Bacteria.objects.all()
    list_display = ('id', 'strain', 'genus', 'species')

class EnvironmentalSampleCollectionAdmin(admin.ModelAdmin):
    queryset = EnvironmentalSampleCollection.objects.all()
    list_display = ('id',)

admin.site.register(Box, BoxAdmin)
admin.site.register(StorageLocation, StorageLocationAdmin)
admin.site.register(Assembly, AssemblyAdmin)
admin.site.register(TubeType, TubeTypeAdmin)
admin.site.register(ExperimentalResult, ExperimentalResultAdmin)
admin.site.register(SequencingRun, SequencingRunAdmin)
admin.site.register(Tube, TubeAdmin)
admin.site.register(SampleType, SampleTypeAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Phage, PhageAdmin)
admin.site.register(PhageDNAPrep, PhageDNAPrepAdmin)
admin.site.register(SequencingRunPool, SequencingRunPoolAdmin)
admin.site.register(SequencingRunPoolItem, SequencingRunPoolItemAdmin)
admin.site.register(ContainerType, ContainerTypeAdmin)
admin.site.register(EnvironmentalSample, EnvironmentalSampleAdmin)
admin.site.register(Lysate, LysateAdmin)
admin.site.register(Bacteria, BacteriaAdmin)
admin.site.register(EnvironmentalSampleCollection, EnvironmentalSampleCollectionAdmin)
