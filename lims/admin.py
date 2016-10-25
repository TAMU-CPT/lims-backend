from django.contrib import admin
from .models import Box, StorageLocation, Assembly, TubeType, ExperimentalResult, SequencingRun, Tube, SampleType, Experiment, Phage, PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, ContainerType, EnvironmentalSample, Lysate, Bacteria

class BoxAdmin(admin.ModelAdmin):
    queryset = Box.objects.all()
    list_display = ('id', 'name', 'location',)

class StorageLocationAdmin(admin.ModelAdmin):
    queryset = StorageLocation.objects.all()
    list_display = ('id', 'name', 'container_type', 'location',)

class AssemblyAdmin(admin.ModelAdmin):
    queryset = Assembly.objects.all()
    list_display = ('notes', 'sequencing_run', 'galaxy_dataset', 'id')

class TubeTypeAdmin(admin.ModelAdmin):
    queryset = TubeType.objects.all()
    list_display = ('name', 'id',)

class ExperimentalResultAdmin(admin.ModelAdmin):
    queryset = ExperimentalResult.objects.all()
    list_display = ('date', 'experiment', 'id', 'run_by', 'result',)

class SequencingRunAdmin(admin.ModelAdmin):
    queryset = SequencingRun.objects.all()
    list_display = ('methods', 'bioanalyzer_qc', 'date', 'galaxy_history', 'run_prep_spreadsheet', 'id', 'name',)

class TubeAdmin(admin.ModelAdmin):
    queryset = Tube.objects.all()
    list_display = ('box', 'type', 'name', 'id',)

class SampleTypeAdmin(admin.ModelAdmin):
    queryset = SampleType.objects.all()
    list_display = ('name', 'id',)

class ExperimentAdmin(admin.ModelAdmin):
    queryset = Experiment.objects.all()
    list_display = ('full_name', 'id', 'short_name', 'methods',)

class PhageAdmin(admin.ModelAdmin):
    queryset = Phage.objects.all()
    list_display = ('historical_names', 'primary_name', 'id',)

class PhageDNAPrepAdmin(admin.ModelAdmin):
    queryset = PhageDNAPrep.objects.all()
    list_display = ('morphology', 'lysate', 'tube', 'id',)

class SequencingRunPoolAdmin(admin.ModelAdmin):
    queryset = SequencingRunPool.objects.all()
    list_display = ('run', 'id', 'pool',)

class SequencingRunPoolItemAdmin(admin.ModelAdmin):
    queryset = SequencingRunPoolItem.objects.all()
    list_display = ('id', 'pool',)

class ContainerTypeAdmin(admin.ModelAdmin):
    queryset = ContainerType.objects.all()
    list_display = ('name', 'id',)

class EnvironmentalSampleAdmin(admin.ModelAdmin):
    queryset = EnvironmentalSample.objects.all()
    list_display = ('description', 'tube', 'sample_type', 'collection', 'id', 'location',)

class LysateAdmin(admin.ModelAdmin):
    queryset = Lysate.objects.all()
    list_display = ('id', 'oldid', 'isolation', 'tube')

class BacteriaAdmin(admin.ModelAdmin):
    queryset = Bacteria.objects.all()
    list_display = ('id', 'strain', 'genus', 'species')

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
