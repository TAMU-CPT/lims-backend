from rest_framework import serializers
from lims.models import Storage, Assembly, \
    ExperimentalResult, SequencingRun, Experiment, Phage, \
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


class LiteStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'room', 'type', 'container_label', 'shelf', 'box', 'sample_label')

    def to_internal_value(self, data):
        storage, _ = Storage.objects.get_or_create(
            room=data['room'],
            type=data['type'],
            container_label=data['container_label'],
            shelf=data['shelf'],
            box=data['box'],
            sample_label=data['sample_label'],
        )
        return storage


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


class PhageDNAPrepSerializer(serializers.ModelSerializer):
    storage = LiteStorageSerializer()

    class Meta:
        model = PhageDNAPrep
        fields = ('id', 'storage', 'experiments', 'phage')


class EnvironmentalSampleSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    location_xy = serializers.SerializerMethodField()
    collected_by = AccountSerializerLight(read_only=True)

    class Meta:
        model = EnvironmentalSample
        fields = ('id', 'description', 'sample_type', 'collection', 'location_xy', 'collected_by', 'default_collection_id')

    def get_location_xy(self, obj):
        # print obj.location.json
        # print obj.location.geojson
        # print obj.location.coords
        return obj.location.coords


class BacteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bacteria
        fields = ('strain', 'genus', 'species', 'id', 'full')

    def to_internal_value(self, data):
        if isinstance(data, dict):
            # find a bacteria with specified genus / species
            if 'id' in data:
                return Bacteria.objects.get(id=data['id'])
        else:
            parts = data.split()
            if len(parts) == 2:
                genus, species = parts
                bacteria, _ = Bacteria.objects.get_or_create(genus=genus, species=species)
                return bacteria

            elif len(parts) == 3:
                genus, species, strain = parts
                bacteria, _ = Bacteria.objects.get_or_create(genus=genus, species=species, strain=strain)
                return bacteria

        raise Exception("Unknown Bacteria")


class PhageSerializerList(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    owner = AccountSerializerLight(read_only=True)

    class Meta:
        model = Phage
        fields = ('historical_names', 'primary_name', 'id', 'owner', 'morphology')


class EnvironmentalSampleCollectionSerializer(NestableSerializer):
    id = serializers.UUIDField(read_only=False)
    true_collection = serializers.SerializerMethodField(read_only=True)
    env_sample = EnvironmentalSampleSerializer(many=True)

    class Meta:
        model = EnvironmentalSampleCollection
        fields = ('id', 'env_sample', 'description', 'storage', 'env_sample', 'true_collection')

    def get_true_collection(self, obj):
        esr = obj.environmentalsamplerelation_set.first()
        return esr.true_collection

    def update(self, instance, validated_data):
        for sample in validated_data['env_sample']:
            es = EnvironmentalSampleSerializer(data=sample)
            #
            print(es.is_valid())
            # es.is_valid(raise_exception=True)
            print(es['id'].value)
        return instance

    def to_internal_value(self, data):
        if isinstance(data, str):
            return EnvironmentalSampleCollection.objects.get(id=data)

        return super(EnvironmentalSampleCollectionSerializer, self).to_internal_value(data)


class LitePhageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phage
        fields = ('id', 'primary_name')


class LysateSerializer(serializers.ModelSerializer):
    env_sample_collection = EnvironmentalSampleCollectionSerializer()
    host = BacteriaSerializer()
    storage = LiteStorageSerializer()
    phage = LitePhageSerializer(read_only=True)

    class Meta:
        model = Lysate
        fields = ('isolation', 'storage', 'id', 'oldid', 'host', 'env_sample_collection', 'phage')


class PhageSerializerDetail(serializers.ModelSerializer):
    host = BacteriaSerializer(many=True)
    assembly = AssemblySerializer(required=False, allow_null=True)
    phagednaprep = PhageDNAPrepSerializer(required=False, allow_null=True)
    lysate = LysateSerializer(required=False, allow_null=True)

    class Meta:
        model = Phage
        fields = (
            'historical_names', 'primary_name', 'id',
            'host', 'owner', 'source', 'assembly', 'phagednaprep', 'lysate'
        )

    def update(self, instance, validated_data):
        host = validated_data['host']
        host_lims_new = []
        for h in host:
            h_obj, created = Bacteria.objects.get_or_create(**h)
            h['id'] = h_obj.id
            host_lims_new.append(h_obj)
        validated_data['host'] = host_lims_new

        # env_sample_collection_new = []
        # for env_sample in validated_data['env_sample_collection']['env_sample']:
            # print env_sample

        for prop in ('historical_names', 'primary_name', 'host', 'source', 'assembly'):
            x = validated_data.get(prop, getattr(instance, prop))
            print('Setattr %s %s = %s' % (instance, prop, x))
            setattr(instance, prop, x)

        instance.save()
        return validated_data


class LysateSerializerDetail(serializers.ModelSerializer):
    phage = PhageSerializerList(read_only=False, allow_null=True)
    frontend_label = serializers.SerializerMethodField()
    env_sample_collection = EnvironmentalSampleCollectionSerializer(read_only=False)

    class Meta:
        model = Lysate
        fields = ('frontend_label', 'isolation', 'storage', 'id', 'oldid', 'host', 'env_sample_collection', 'phage')

    def get_frontend_label(self, obj):
        return 'lysate'


class BasicLysateSerializer(serializers.ModelSerializer):
    frontend_label = serializers.SerializerMethodField()
    # phage = PhageSerializerList(read_only=False, allow_null=True)
    phage_set = serializers.SerializerMethodField()

    class Meta:
        model = Lysate
        fields = ('frontend_label', 'id', 'phage_set')

    def get_frontend_label(self, obj):
        return 'lysate'

    def get_phage_set(self, obj):
        try:
            phage = obj.phage
            return [PhageSerializerList(phage).data]
        except Phage.DoesNotExist:
            pass


class PhageDNAPrepSerializerDetail(serializers.ModelSerializer):
    experiments = ExperimentalResultDetailSerializer(many=True, read_only=True)
    assembly_set = AssemblySerializer(many=True, read_only=True)
    phage_set = PhageSerializerList(read_only=False, allow_null=True, many=True)
    frontend_label = serializers.SerializerMethodField()

    class Meta:
        model = PhageDNAPrep
        fields = ('frontend_label', 'morphology', 'experiments', 'storage', 'id', 'assembly_set', 'phage_set')

    def get_frontend_label(self, obj):
        return 'phagednaprep'


class BasicPhageDNAPrepSerializer(serializers.ModelSerializer):
    frontend_label = serializers.SerializerMethodField()
    phage_set = PhageSerializerList(read_only=False, allow_null=True, many=True)

    class Meta:
        model = Lysate
        fields = ('frontend_label', 'id', 'phage_set')

    def get_frontend_label(self, obj):
        return 'phagednaprep'


class BasicEnvironmentalSampleCollectionSerializer(NestableSerializer):
    frontend_label = serializers.SerializerMethodField()
    phage_set = serializers.SerializerMethodField()

    class Meta:
        model = EnvironmentalSampleCollection
        fields = ('frontend_label', 'id', 'phage_set')

    def get_frontend_label(self, obj):
        return 'envsample'

    def get_phage_set(self, obj):
        try:
            phages = []
            lysate_set = obj.lysate_set
            for lysate in lysate_set.all():
                try:
                    phage = lysate.phage
                    phages.append(PhageSerializerList(phage).data)
                except:
                    pass
            if len(phages) > 0:
                return phages
        except Lysate.DoesNotExist:
            pass


class StorageSerializer(serializers.ModelSerializer):
    sample_category = serializers.SerializerMethodField()

    class Meta:
        model = Storage
        fields = ('id', 'room', 'type', 'container_label', 'shelf', 'box', 'sample_label', 'sample_category')

    def get_sample_category(self, obj):
        if obj.what_category == 'lysate':
            return BasicLysateSerializer(obj.lysate).data
        elif obj.what_category == 'phagednaprep':
            return BasicPhageDNAPrepSerializer(obj.phagednaprep).data
        elif obj.what_category == 'envsample':
            return BasicEnvironmentalSampleCollectionSerializer(obj.environmentalsamplecollection).data
        else:
            return

    def to_internal_value(self, data):
        print('asdf')
        if isinstance(data, dict):
            if 'id' in dict:
                raise Exception("Please double check me!")

            storage, _ = Storage.objects.get_or_create(
                room=data['room'],
                type=data['type'],
                container_label=data['container_label'],
                shelf=data['shelf'],
                box=data['box'],
                sample_label=data['sample_label'],
            )
            return storage

        raise Exception("Please double check me!")


class RoomStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('room',)


class ContainerLabelStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('container_label',)


class BoxStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('box',)
