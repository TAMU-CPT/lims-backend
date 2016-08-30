from web.models import Assembly, Bacteria, Box, ContainerType, EnvironmentalSample, Experiment, ExperimentalResult, Lysate, PhageDNAPrep, SampleType, SequencingRun, SequencingRunPool, SequencingRunPoolItem, StorageLocation, Tube, TubeType
from rest_framework import serializers


class TubeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TubeType
        fields = (
            'id', 'name'
        )
class TubeSerializer(serializers.ModelSerializer):
    type = TubeTypeSerializer(read_only=True)

    class Meta:
        model = Tube
        fields = (
            'id', 'name', 'box', 'type'
        )

class AssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assembly
        fields = (
            'id', 'dna_prep', 'sequencing_run', 'galaxy_dataset', 'notes'
        )

class BacteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bacteria
        fields = (
            'id', 'genus', 'species', 'strain'
        )

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = (
            'id', 'name', 'location'
        )

class ContainerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerType
        fields = (
            'id', 'name'
        )

class EnvironmentalSampleSerializer(serializers.ModelSerializer):
    tube = TubeSerializer(read_only=True)

    class Meta:
        model = EnvironmentalSample
        fields = (
            'id', 'description', 'collection', 'location', 'sample_type', 'tube'
        )

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = (
            'id', 'short_name', 'full_name', 'methods'
        )

class ExperimentalResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentalResult
        fields = (
            'id', 'experiment', 'result', 'date', 'run_by'
        )

class LysateSerializer(serializers.ModelSerializer):
    tube = TubeSerializer(read_only=True)

    class Meta:
        model = Lysate
        fields = (
            'id', 'env_sample', 'oldid', 'isolation', 'owner', 'source', 'tube'
        )

class PhageDNAPrepSerializer(serializers.ModelSerializer):
    tube = TubeSerializer(read_only=True)

    class Meta:
        model = PhageDNAPrep
        fields = (
            'id', 'lysate', 'morphology', 'tube'
        )

class SampleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleType
        fields = (
            'id', 'name'
        )

class SequencingRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRun
        fields = (
            'id', 'galaxy_history', 'name', 'date', 'methods', 'bioanalyzer_qc', 'run_prep_spreadsheet'
        )

class SequencingRunPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRunPool
        fields = (
            'id', 'pool', 'run'
        )

class SequencingRunPoolItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRunPoolItem
        fields = (
            'id', 'pool', 'phage', 'dna_conc'
        )

class StorageLocationSerializer(serializers.ModelSerializer):
    container_type = serializers.SerializerMethodField()
    class Meta:
        model = StorageLocation
        fields = (
            'id', 'name', 'location', 'container_type', 'box_set'
        )

    def get_container_type(self, obj):
        return obj.container_type.name

class StorageLocationDetailSerializer(serializers.ModelSerializer):
    boxen = serializers.SerializerMethodField()
    class Meta:
        model = StorageLocation
        fields = (
            'id', 'name', 'location', 'container_type', 'boxen'
        )

    def get_boxen(self, obj):
        for box in obj.box_set.all():
            yield BoxSerializer(box).data

class BoxDetailSerializer(serializers.ModelSerializer):
    env_sample = serializers.SerializerMethodField()
    lysate = serializers.SerializerMethodField()
    dna_prep = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = (
            'id', 'name', 'location', 'env_sample', 'lysate', 'dna_prep'
        )

    def get_env_sample(self, obj):
        for tube in obj.getEnvironmentalTubes():
            yield EnvironmentalSampleSerializer(tube.environmentalsample).data

    def get_lysate(self, obj):
        for tube in obj.getLysateTubes():
            yield LysateSerializer(tube.lysate).data

    def get_dna_prep(self, obj):
        for tube in obj.getPhageDNAPrepTubes():
            yield PhageDNAPrepSerializer(tube.phagednaprep).data
