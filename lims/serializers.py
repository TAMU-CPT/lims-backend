from rest_framework import serializers
from lims.models import Storage, Assembly, \
    ExperimentalResult, SequencingRun, SampleType, Experiment, Phage, \
    PhageDNAPrep, SequencingRunPool, SequencingRunPoolItem, \
    EnvironmentalSample, Lysate, Bacteria, EnvironmentalSampleCollection
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator
from account.serializers import AccountSerializerLight


class NestableSerializer(serializers.ModelSerializer):
    """
    Use this when "This field must be unique" on child models.
    """

    def to_internal_value(self, data):
        # https://github.com/tomchristie/django-rest-framework/issues/2403#issuecomment-95528016
        if 'id' in data and 'id' in self.fields:
            try:
                obj_id = self.fields['id'].to_internal_value(data['id'])
            except ValidationError as exc:
                raise ValidationError({'id': exc.detail})
            for field in self.fields.values():
                for validator in field.validators:
                    if type(validator) == UniqueValidator:
                        # Exclude id from queryset for checking uniqueness
                        validator.queryset = validator.queryset.exclude(id=obj_id)
        return super(NestableSerializer, self).to_internal_value(data)



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
    # TODO
    methods = SeqRunExperimentSerializer(read_only=True)
    owner = AccountSerializerLight(read_only=True)

    class Meta:
        model = SequencingRun
        fields = ('methods', 'bioanalyzer_qc', 'date', 'galaxy_history', 'run_prep_spreadsheet', 'id', 'name', 'owner')


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

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'room', 'type', 'name', 'shelf', 'box', 'tube', 'tube_type',)

class AssemblySerializer(serializers.ModelSerializer):
    sequencing_run_pool_item = SequencingRunPoolItemSerializer()

    class Meta:
        model = Assembly
        fields = ('notes', 'sequencing_run_pool_item', 'galaxy_dataset', 'id')


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ('full_name', 'id', 'short_name', 'methods', 'category')


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
        fields = ('morphology', 'id', 'storage', 'experiments')


class PhageDNAPrepSerializerDetail(serializers.ModelSerializer):
    experiments = ExperimentalResultDetailSerializer(many=True, read_only=True)
    assembly_set = AssemblySerializer(many=True, read_only=True)

    class Meta:
        model = PhageDNAPrep
        fields = ('morphology', 'experiments', 'storage', 'id')


class EnvironmentalSampleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    sample_type = SampleTypeSerializer()
    location_xy = serializers.SerializerMethodField()
    collected_by = AccountSerializerLight(read_only=True)

    class Meta:
        model = EnvironmentalSample
        fields = ('description', 'storage', 'sample_type', 'collection', 'id', 'location', 'location_xy', 'collected_by')

    def get_location_xy(self, obj):
        # print obj.location.json
        # print obj.location.geojson
        # print obj.location.coords
        return obj.location.coords

    def create(self, validated_data):
        print 'ess, create', validated_data

    def update(self, instance, validated_data):
        print instance
        print validated_data
        return instance


class LysateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lysate
        fields = ('isolation', 'storage', 'phage', 'id', 'oldid',)


class BacteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bacteria
        fields = ('strain', 'genus', 'species', 'id',)


class LysateSerializerDetail(serializers.ModelSerializer):

    class Meta:
        model = Lysate
        fields = ('isolation', 'storage', 'phage', 'id', 'oldid')


class PhageSerializerList(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Phage
        fields = ('historical_names', 'primary_name', 'id')


class EnvironmentalSampleCollectionSerializer(NestableSerializer):
    id = serializers.UUIDField(read_only=False)
    env_sample = EnvironmentalSampleSerializer(many=True)

    class Meta:
        model = EnvironmentalSampleCollection
        fields = ('id', 'env_sample', 'description')

    def update(self, instance, validated_data):

        for sample in validated_data['env_sample']:
            es = EnvironmentalSampleSerializer(data=sample)
            #
            print es.is_valid()
            # es.is_valid(raise_exception=True)
            print es['id'].value


            # print sample
            # print es
            # print dir(es)
            # print es.object
            # print dir(es)
        # print instance
        # print validated_data
        return instance


class PhageSerializerDetail(serializers.ModelSerializer):
    env_sample_collection = EnvironmentalSampleCollectionSerializer(read_only=False)
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
