
from rest_framework import serializers
from lims.models import Box, StorageLocation, Assembly, TubeType, \
    ExperimentalResult, SequencingRun, Tube, SampleType, Experiment, Phage, \
    PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, ContainerType, \
    EnvironmentalSample, Lysate, Bacteria, EnvironmentalSampleCollection


class SeqRunExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ('full_name', 'id', 'short_name', 'methods',)

class SeqRunExperimentalResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentalResult
        fields = ('date', 'experiment', 'id', 'run_by', 'result',)

class SeqRunExperimentalResultDetailSerializer(serializers.ModelSerializer):
    experiment = SeqRunExperimentSerializer()
    class Meta:
        model = ExperimentalResult
        fields = ('date', 'experiment', 'id', 'run_by', 'result',)

class SequencingRunSerializer(serializers.ModelSerializer):
    methods = SeqRunExperimentSerializer()

    class Meta:
        model = SequencingRun
        fields = ('methods', 'bioanalyzer_qc', 'date', 'galaxy_history', 'run_prep_spreadsheet', 'id', 'name',)

class SequencingRunPoolSerializer(serializers.ModelSerializer):
    run = SequencingRunSerializer()
    class Meta:
        model = SequencingRunPool
        fields = ('run', 'id', 'pool',)

class SequencingRunPoolItemSerializer(serializers.ModelSerializer):
    # dna_conc = SeqRunExperimentalResultDetailSerializer(many=True)
    pool = SequencingRunPoolSerializer()

    class Meta:
        model = SequencingRunPoolItem
        fields = ('id', 'pool',)

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
    sequencing_run_pool_item = SequencingRunPoolItemSerializer()
    class Meta:
        model = Assembly
        fields = ('notes', 'sequencing_run_pool_item', 'galaxy_dataset', 'id')

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

class SampleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleType
        fields = ('name', 'id',)

class PhageDNAPrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhageDNAPrep
        fields = ('morphology', 'id', 'tube', 'experiments')

class PhageDNAPrepSerializerDetail(serializers.ModelSerializer):
    tube = TubeSerializer()
    experiments = ExperimentalResultDetailSerializer(many=True, read_only=True)
    assembly_set = AssemblySerializer(many=True, read_only=True)

    class Meta:
        model = PhageDNAPrep
        fields = ('morphology', 'experiments', 'tube', 'id')

class ContainerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerType
        fields = ('name', 'id',)

class EnvironmentalSampleSerializer(serializers.ModelSerializer):
    tube = TubeSerializer()
    sample_type = SampleTypeSerializer()

    class Meta:
        model = EnvironmentalSample
        fields = ('description', 'tube', 'sample_type', 'collection', 'id', 'location',)

class LysateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lysate
        fields = ('isolation', 'tube', 'phage', 'id', 'oldid',)

class BacteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bacteria
        fields = ('strain', 'genus', 'species', 'id',)

class LysateSerializerDetail(serializers.ModelSerializer):
    tube = TubeSerializer()

    class Meta:
        model = Lysate
        fields = ('isolation', 'tube', 'phage', 'id', 'oldid')

class PhageSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Phage
        fields = ('historical_names', 'primary_name', 'id')


class EnvironmentalSampleCollectionSerializer(serializers.ModelSerializer):
    env_sample = EnvironmentalSampleSerializer(many=True, read_only=True)

    class Meta:
        model = EnvironmentalSampleCollection
        fields = ('id', 'env_sample')

class PhageSerializerDetail(serializers.ModelSerializer):
    lysate = LysateSerializerDetail()
    env_sample_collection = EnvironmentalSampleCollectionSerializer()
    host_lims = BacteriaSerializer(many=True)
    # owner =
    # source =
    assembly = AssemblySerializer()

    class Meta:
        model = Phage
        fields = (
            'historical_names', 'primary_name', 'id', 'lysate',
            'env_sample_collection', 'host_lims', 'owner', 'source', 'assembly',
        )
