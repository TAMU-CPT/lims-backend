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
    location_xy = serializers.SerializerMethodField()

    class Meta:
        model = EnvironmentalSample
        fields = ('description', 'tube', 'sample_type', 'collection', 'id', 'location', 'location_xy')

    def get_location_xy(self, obj):
        # print obj.location.json
        # print obj.location.geojson
        # print obj.location.coords
        return obj.location.coords


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
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Phage
        fields = ('historical_names', 'primary_name', 'id')


class EnvironmentalSampleCollectionSerializer(serializers.ModelSerializer):
    env_sample = EnvironmentalSampleSerializer(many=True, read_only=True)

    class Meta:
        model = EnvironmentalSampleCollection
        fields = ('id', 'env_sample')


class PhageSerializerDetail(serializers.ModelSerializer):
    env_sample_collection = EnvironmentalSampleCollectionSerializer(required=False, allow_null=True, partial=True)
    host_lims = BacteriaSerializer(many=True)
    assembly = AssemblySerializer(required=False, allow_null=True)
    phagednaprep = PhageDNAPrepSerializer(required=False, allow_null=True)

    class Meta:
        model = Phage
        fields = (
            'historical_names', 'primary_name', 'id', 'env_sample_collection',
            'host_lims', 'owner', 'source', 'assembly', 'phagednaprep'
        )

    def update(self, instance, validated_data):
        import pprint; pprint.pprint(validated_data)
        host_lims = validated_data['host_lims']
        host_lims_new = []
        for host in host_lims:
            host_obj, created = Bacteria.objects.get_or_create(**host)
            host['id'] = host_obj.id
            host_lims_new.append(host_obj)
        validated_data['host_lims'] = host_lims_new

        env_sample_collection_new = []
        # for env_sample in validated_data['env_sample_collection']['env_sample']:
            # print env_sample

        for prop in ('historical_names', 'primary_name', 'host_lims', 'source', 'assembly'):
            x = validated_data.get(prop, getattr(instance, prop))
            print 'Setattr %s %s = %s' % (instance, prop, x)
            setattr(instance, prop, x)

        instance.save()
        return validated_data
