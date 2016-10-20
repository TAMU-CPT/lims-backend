
from rest_framework import serializers
from lims.models import Box, StorageLocation, Assembly, TubeType, ExperimentalResult, SequencingRun, Tube, SampleType, Experiment, Phage, PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, ContainerType, EnvironmentalSample, Lysate, Bacteria

class BoxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Box
        fields = ('id', 'name', 'location',)

class StorageLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StorageLocation
        fields = ('id', 'name', 'container_type', 'location',)

class AssemblySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assembly
        fields = ('notes', 'sequencing_run', 'galaxy_dataset', 'id', 'dna_prep',)

class TubeTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TubeType
        fields = ('name', 'id',)

class ExperimentalResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExperimentalResult
        fields = ('date', 'experiment', 'id', 'run_by', 'result',)

class SequencingRunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SequencingRun
        fields = ('methods', 'bioanalyzer_qc', 'date', 'galaxy_history', 'run_prep_spreadsheet', 'id', 'name',)

class TubeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tube
        fields = ('box', 'type', 'name', 'id',)

class SampleTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SampleType
        fields = ('name', 'id',)

class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experiment
        fields = ('full_name', 'id', 'short_name', 'methods',)

class PhageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phage
        fields = ('historical_names', 'primary_name', 'id',)

class PhageDNAPrepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhageDNAPrep
        fields = ('morphology', 'lysate', 'experiments', 'tube', 'id',)

class SequencingRunPoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SequencingRunPool
        fields = ('run', 'id', 'pool',)

class SequencingRunPoolItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SequencingRunPoolItem
        fields = ('dna_conc', 'phage', 'id', 'pool',)

class ContainerTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContainerType
        fields = ('name', 'id',)

class EnvironmentalSampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EnvironmentalSample
        fields = ('description', 'tube', 'sample_type', 'collection', 'id', 'location',)

class LysateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lysate
        fields = ('isolation', 'tube', 'source', 'phage', 'host_lims', 'owner', 'env_sample', 'id', 'oldid',)

class BacteriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bacteria
        fields = ('strain', 'genus', 'species', 'id',)
