from lims.models import Assembly, Bacteria, Box, ContainerType, EnvironmentalSample, Experiment, ExperimentalResult, Lysate, PhageDNAPrep, SampleType, SequencingRun, SequencingRunPool, SequencingRunPoolItem, StorageLocation, Tube, TubeType
from rest_framework import serializers
from directory.serializers import AccountSerializer, AccountLessOrgSerializer


class SampleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleType
        fields = (
            'id', 'name'
        )

class TubeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TubeType
        fields = (
            'id', 'name'
        )
class TubeSerializer(serializers.ModelSerializer):
    type = TubeTypeSerializer(read_only=True)
    location = serializers.SerializerMethodField()

    class Meta:
        model = Tube
        fields = (
            'id', 'name', 'type', 'location'
        )

    def get_location(self, obj):
        return {
            'tube_id': obj.id,
            'tube_name': obj.name,
            'box_id': obj.box.id,
            'box_name': obj.box.name,
            'storage_id': obj.box.location.id,
            'storage_name': obj.box.location.name,
        }

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
    sample_type = SampleTypeSerializer(read_only=True)
    latlon = serializers.SerializerMethodField()

    class Meta:
        model = EnvironmentalSample
        fields = (
            'id', 'description', 'collection', 'location', 'sample_type', 'tube', 'latlon',
        )

    def get_latlon(self, obj):
        return obj.location.get_coords()

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
    env_sample_data = serializers.SerializerMethodField()
    hosts = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    owner = AccountSerializer(read_only=True)
    source = AccountLessOrgSerializer(read_only=True)

    class Meta:
        model = Lysate
        fields = (
            'id', 'oldid', 'isolation', 'owner', 'source',
            'tube', 'env_sample_data', 'hosts', 'name'
        )

    def get_env_sample_data(self, obj):
        for env_sample in obj.env_sample.all():
            yield EnvironmentalSampleSerializer(env_sample).data

    def get_hosts(self, obj):
        for host in obj.host_lims.all():
            yield BacteriaSerializer(host).data

    def get_name(self, obj):
        return str(obj)

class PhageDNAPrepSerializer(serializers.ModelSerializer):
    tube = TubeSerializer(read_only=True)
    morphology = serializers.SerializerMethodField()
    lysate = LysateSerializer(read_only=True)

    class Meta:
        model = PhageDNAPrep
        fields = (
            'id', 'lysate', 'morphology', 'tube'
        )

    def get_morphology(self, obj):
        return obj.get_morphology_display()

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
