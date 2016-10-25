
from rest_framework import serializers
from lims.models import Box, StorageLocation, Assembly, TubeType, ExperimentalResult, SequencingRun, Tube, SampleType, Experiment, Phage, PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, ContainerType, EnvironmentalSample, Lysate, Bacteria

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('id', 'name', 'location',)

class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = ('id', 'name', 'container_type', 'location',)

class AssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assembly
        fields = ('notes', 'sequencing_run', 'galaxy_dataset', 'id', 'dna_prep',)

class TubeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TubeType
        fields = ('name', 'id',)

class ExperimentalResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentalResult
        fields = ('date', 'experiment', 'id', 'run_by', 'result',)

class SequencingRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRun
        fields = ('methods', 'bioanalyzer_qc', 'date', 'galaxy_history', 'run_prep_spreadsheet', 'id', 'name',)

class TubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tube
        fields = ('box', 'type', 'name', 'id',)

class SampleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleType
        fields = ('name', 'id',)

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ('full_name', 'id', 'short_name', 'methods',)

class PhageDNAPrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhageDNAPrep
        fields = ('morphology', 'lysate', 'experiments', 'tube', 'id',)

class SequencingRunPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRunPool
        fields = ('run', 'id', 'pool',)

class SequencingRunPoolItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRunPoolItem
        fields = ('dna_conc', 'phage', 'id', 'pool',)

class ContainerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerType
        fields = ('name', 'id',)

class EnvironmentalSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalSample
        fields = ('description', 'tube', 'sample_type', 'collection', 'id', 'location',)

class LysateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lysate
        fields = ('isolation', 'tube', 'source', 'phage', 'host_lims', 'owner', 'env_sample', 'id', 'oldid',)

class BacteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bacteria
        fields = ('strain', 'genus', 'species', 'id',)

class PhageSerializer(serializers.ModelSerializer):
    lysate = serializers.SerializerMethodField()
    phagednaprep = serializers.SerializerMethodField()
    env_sample = serializers.SerializerMethodField()

    class Meta:
        model = Phage
        fields = (
            'historical_names', 'primary_name', 'id',
            'lysate', 'phagednaprep', 'env_sample',
        )

    def get_lysate(self, obj):
        return LysateSerializer(obj.lysate).data

    def get_phagednaprep(self, obj):
        return PhageDNAPrepSerializer(obj.lysate.phagednaprep).data

    def get_env_sample(self, obj):
        return EnvironmentalSampleSerializer(obj.lysate.env_sample).data
