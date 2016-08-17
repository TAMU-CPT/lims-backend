from web.models import Assembly, Bacteria, Box, ContainerType, EnvironmentalSample, Experiment, ExperimentalResult, Lysate, PhageDNAPrep, SampleType, SequencingRun, SequencingRunPool, SequencingRunPoolItem, StorageLocation, Tube, TubeType
from rest_framework import serializers

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
    class Meta:
        model = EnvironmentalSample
        fields = (
            'id', 'name', 'description', 'collection', 'location', 'sample_type', 'tube'
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
    class Meta:
        model = Lysate
        fields = (
            'id', 'env_sample', 'oldid', 'isolation', 'owner', 'source', 'tube'
        )

class PhageDNAPrepSerializer(serializers.ModelSerializer):
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
            'id', 'pool'
        )

class SequencingRunPoolItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SequencingRunPoolItem
        fields = (
            'id', 'pool', 'phage', 'dna_conc'
        )

class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = (
            'id', 'name', 'location', 'container_type'
        )

class TubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tube
        fields = (
            'id', 'name', 'box', 'type'
        )

class TubeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TubeType
        fields = (
            'id', 'name'
        )

