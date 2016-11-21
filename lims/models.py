# encoding: utf-8
from __future__ import unicode_literals
import uuid
from django.db import models
from directory.models import Organisation
from account.models import Account
from django.core.urlresolvers import reverse_lazy
from django.contrib.gis.db import models as gis_models
from django.utils.encoding import smart_unicode


PHAGE_MORPHOLOGY = (
    (0, 'Unknown'),
    (1, 'Podophage'),
    (2, 'Myophage'),
    (3, 'Siphophage')
)
EXP_RESULT_TYPES = (
    (0, 'Float'),
    (1, 'Integer'),
    (2, 'FloatArray'),
    (3, 'ImageURL')
)


class ContainerType(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return smart_unicode(self.name)


class TubeType(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return smart_unicode(self.name)


class SampleType(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return smart_unicode(self.name)


class StorageLocation(models.Model):
    # HAS_CPT_HASHID
    # Human readable name that gets written on it
    name = models.CharField(max_length=64)
    # Human readable location
    location = models.CharField(max_length=64)
    # Type of container
    container_type = models.ForeignKey(ContainerType)

    def __unicode__(self):
        return smart_unicode(u'{} in {}'.format(self.name, self.location))

    def get_absolute_url(self):
        return reverse_lazy('lims:storage-location-detail', args=[self.id])


class Box(models.Model):
    # HAS_CPT_HASHID
    # Human readable name that gets written on it
    name = models.CharField(max_length=64, help_text="The name which is written on the outside of the box.")
    location = models.ForeignKey(StorageLocation)

    def __unicode__(self):
        return smart_unicode(u'{} in {}'.format(self.name, self.location))

    class Meta:
        verbose_name_plural = "boxes"

    def getEnvironmentalTubes(self):
        return self.tube_set.all().exclude(environmentalsample__isnull=True)

    def getLysateTubes(self):
        return self.tube_set.all().exclude(lysate__isnull=True)

    def getPhageDNAPrepTubes(self):
        return self.tube_set.all().exclude(phagednaprep__isnull=True)

    def get_absolute_url(self):
        return reverse_lazy('lims:box-detail', args=[self.location.id, self.id])


class Tube(models.Model):
    # Human readable name that gets written on it
    name = models.CharField(max_length=64)
    box = models.ForeignKey(Box)
    type = models.ForeignKey(TubeType)

    def __unicode__(self):
        return smart_unicode(u'{} in {}'.format(self.name, self.box))

    def getType(self):
        rType = None
        if self.environmentalsample is not None:
            rType = 'envsample'
        elif self.phagednaprep is not None:
            if rType is not None:
                raise Exception("More than one sample stored in tube")
            else:
                rType = 'dnaprep'
        elif self.lystate is not None:
            if rType is not None:
                raise Exception("More than one sample stored in tube")
            else:
                rType = 'lysate'

        return rType

    def get_absolute_url(self):
        return reverse_lazy('lims:box-detail', args=[self.box.location.id, self.box.id])


class EnvironmentalSample(models.Model):
    description = models.TextField(blank=True)
    # HAS_CPT_HASHID
    collection = models.DateTimeField()
    # location = models.
    location = gis_models.PointField()
    sample_type = models.ForeignKey(SampleType)

    # Tube Storage
    tube = models.OneToOneField(Tube)

    def __unicode__(self):
        return smart_unicode(u'{} sample from {}'.format(self.sample_type, self.collection))

    def get_absolute_url(self):
        return reverse_lazy('lims:envsample-detail', args=[self.id])


class Bacteria(models.Model):
    genus = models.CharField(max_length=64)
    species = models.CharField(max_length=64, blank=True)
    strain = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        if self.strain:
            return smart_unicode(u'{}. {} spp {}'.format(self.genus[0], self.species, self.strain))
        return smart_unicode(u'{}. {}'.format(self.genus[0], self.species))

    class Meta:
        verbose_name_plural = "bacteria"

    def get_absolute_url(self):
        return reverse_lazy('lims:bacteria-detail', args=[self.id])


class Lysate(models.Model):
    # HAS_CPT_HASHID
    oldid = models.CharField(max_length=64, blank=True)
    isolation = models.DateTimeField(null=True, blank=True)
    phage = models.OneToOneField('Phage')

    # Tube Storage
    tube = models.OneToOneField(Tube)

    def __unicode__(self):
        return smart_unicode(u'Lysate from {}'.format(self.phage.env_sample_collection))

    def get_absolute_url(self):
        return reverse_lazy('lims:lysate-detail', args=[self.id])


class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_name = models.CharField(max_length=32)
    full_name = models.TextField()
    methods = models.TextField()
    category = models.TextField(blank=True)

    def __unicode__(self):
        return smart_unicode(self.short_name)


class ExperimentalResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experiment = models.ForeignKey(Experiment)
    result = models.TextField()
    date = models.DateTimeField()
    run_by = models.ForeignKey(Account)
    # result_type = models.IntegerField(choices=EXP_RESULT_TYPES)

    def __unicode__(self):
        return smart_unicode(u'{} - {}'.format(
            self.experiment.short_name,
            self.result
        ))


class PhageDNAPrep(models.Model):
    # HAS_CPT_HASHID
    lysate = models.OneToOneField(Lysate, blank=True, null=True)
    phage = models.OneToOneField('Phage')

    morphology = models.IntegerField(choices=PHAGE_MORPHOLOGY)

    # These will point to OMERO eventually...
    # tem_image = models.URLField()
    # gel_image = models.URLField()
    # Nanodrop, pico green, other?
    experiments = models.ManyToManyField(ExperimentalResult, blank=True)

    # Tube Storage
    tube = models.OneToOneField(Tube)

    def __unicode__(self):
        return u'Prep of %s with %s morphology' % (self.lysate, smart_unicode(self.get_morphology_display()))

    def get_absolute_url(self):
        return reverse_lazy('lims:phagedna-detail', args=[self.id])


class SequencingRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    galaxy_history = models.URLField()
    name = models.TextField()
    date = models.DateField()
    # Illumina, miseq, etc need to be in experiments
    methods = models.ForeignKey(Experiment)
    bioanalyzer_qc = models.TextField()
    run_prep_spreadsheet = models.URLField()
    owner = models.ForeignKey(Account, blank=True, null=True)

    def __unicode__(self):
        return smart_unicode(u'{} on {}'.format(self.name, self.date))


class SequencingRunPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pool = models.CharField(max_length=16)
    run = models.ForeignKey(SequencingRun)

    class Meta:
        unique_together = (('pool', 'run'),)

    def __unicode__(self):
        return smart_unicode(u'Run "{0.run.name}" Pool {0.pool}'.format(self))

    def numPhages(self):
        return self.sequencingrunpoolitem_set.count()

    def totalGenomeSize(self):
        return sum([poolitem.phage.expected_size() for poolitem in self.sequencingrunpoolitem_set.objects.all()])

    def expectedFullCoverageFromFLXTiFullPlate(self):
        if self.numPhages() > 0:
            return 60000000 / self.totalGenomeSize()
        else:
            return 0

    def expectedDnaConcInFinalUndilultedMix(self, desiredSize):
        if self.poolSize() > 0:
            a = sum([poolitem.volumeInMix(desiredSize) for poolitem in self.sequencingrunpoolitem_set.objects.all()])
            b = sum([poolitem.ngDnaInMix(poolitem.volumeInMix(desiredSize)) for poolitem in self.sequencingrunpoolitem_set.objects.all()])
            return b / a
        return 0

    def poolSize(self):
        return self.sequencingrunpoolitem_set.count

    def meanGenomeSize(self):
        if self.poolSize() > 0:
            return sum([poolitem.phage.expected_size() for poolitem in self.sequencingrunpoolitem_set.objects.all()]) / self.poolSize()
        return 0


class SequencingRunPoolItem(models.Model):
    pool = models.ForeignKey(SequencingRunPool)
    dna_conc = models.ForeignKey(ExperimentalResult, blank=True)

    def volumeInMix(self, desiredSize):
        if self.pool.poolSize() > 0:
            return (desiredSize * self.dna_conc) / (self.phage.expected_size() / self.pool.totalGenomeSize())
        return 0

    def ngDnaInMix(self, volumeInMix):
        return volumeInMix * self.dna_conc


class Assembly(models.Model):
    """
    This represents a single assembly run of a single genome's sequencing data
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sequencing_run_pool_item = models.ForeignKey(SequencingRunPoolItem, blank=True, null=True)
    galaxy_dataset = models.URLField()
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "assemblies"

    def __unicode__(self):
        return 'Assembly %s' % self.id


class EnvironmentalSampleCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    env_sample = models.ManyToManyField(EnvironmentalSample, blank=True)


class Phage(models.Model):
    primary_name = models.CharField(max_length=64)
    historical_names = models.TextField(blank=True, null=True)  # JSON encoded list of old names
    env_sample_collection = models.ForeignKey(EnvironmentalSampleCollection, blank=True, null=True)
    host_lims = models.ManyToManyField(Bacteria, blank=True)
    owner = models.ForeignKey(Account, blank=True, null=True)
    source = models.ForeignKey(Organisation, blank=True, null=True)
    assembly = models.ForeignKey(Assembly, blank=True, null=True)
