
from rest_framework import serializers
from lims.models import Box, StorageLocation, Assembly, TubeType, ExperimentalResult, SequencingRun, Tube, SampleType, Experiment, Phage, PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, ContainerType, EnvironmentalSample, Lysate, Bacteria

class TubeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TubeType
        fields = ('name', 'id',)

class TubeSerializer(serializers.ModelSerializer):
    type = TubeTypeSerializer()

    class Meta:
        model = Tube
        fields = ('box', 'type', 'name', 'id',)

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

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ('full_name', 'id', 'short_name', 'methods',)

class ExperimentalResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentalResult
        fields = ('date', 'experiment', 'id', 'run_by', 'result',)

class ExperimentalResultDetailSerializer(serializers.ModelSerializer):
    experiment = ExperimentSerializer()
    class Meta:
        model = ExperimentalResult
        fields = ('date', 'experiment', 'id', 'run_by', 'result',)

class SequencingRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRun
        fields = ('methods', 'bioanalyzer_qc', 'date', 'galaxy_history', 'run_prep_spreadsheet', 'id', 'name',)

class SampleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleType
        fields = ('name', 'id',)

class PhageDNAPrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhageDNAPrep
        fields = ('morphology', 'lysate', 'experiments', 'tube', 'id',)

class PhageDNAPrepSerializerDetail(serializers.ModelSerializer):
    tube = TubeSerializer()
    experiments = ExperimentalResultDetailSerializer(many=True, read_only=True)
    assembly_set = AssemblySerializer(many=True, read_only=True)

    class Meta:
        model = PhageDNAPrep
        fields = ('morphology', 'lysate', 'experiments', 'tube', 'id', 'assembly_set')

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
    tube = TubeSerializer()

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

class LysateSerializerDetail(serializers.ModelSerializer):
    tube = TubeSerializer()
    host_lims = BacteriaSerializer(many=True, read_only=True)
    env_sample = EnvironmentalSampleSerializer(many=True, read_only=True)
    phagednaprep =PhageDNAPrepSerializerDetail()

    class Meta:
        model = Lysate
        fields = ('isolation', 'tube', 'source', 'phage', 'host_lims', 'owner', 'env_sample', 'id', 'oldid', 'phagednaprep')

class PhageSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Phage
        fields = ('historical_names', 'primary_name', 'id')

class PhageSerializerDetail(serializers.ModelSerializer):
    lysate = LysateSerializerDetail()

    class Meta:
        model = Phage
        fields = (
            'historical_names', 'primary_name', 'id', 'lysate'
        )
