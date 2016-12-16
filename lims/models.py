# encoding: utf-8
from __future__ import unicode_literals
import uuid
from django.db import models
from directory.models import Organisation
from account.models import Account
from django.core.urlresolvers import reverse_lazy
from django.contrib.gis.db import models as gis_models
from django.db.models import signals


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
STORAGE_TYPES = (
    (0, 'Fridge'),
    (1, 'Freezer')
)

class SampleType(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Storage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.CharField(max_length=32) # e.g. '315'
    type = models.IntegerField(choices=STORAGE_TYPES)
    container_label = models.CharField(max_length=64) # e.g. '315 F5' (or whatever the fridge/freezer label says)
    shelf = models.CharField(max_length=32, blank=True, null=True)
    box = models.CharField(max_length=64, blank=True, null=True) # label on box, if there is one
    sample_label = models.CharField(max_length=64) # label on tube

    def __unicode__(self):
        return self.container_label

    @property
    def what_category(self):
        try:
            lysate = self.lysate
            return 'lysate'
        except Lysate.DoesNotExist:
            pass

        try:
            phagednaprep = self.phagednaprep
            return 'phagednaprep'
        except PhageDNAPrep.DoesNotExist:
            pass

        try:
            envsample = self.environmentalsamplecollection
            return 'envsample'
        except EnvironmentalSampleCollection.DoesNotExist:
            pass

        return


class EnvironmentalSample(models.Model):
    description = models.TextField(blank=True)
    collection = models.DateTimeField()
    location = gis_models.PointField()
    sample_type = models.ForeignKey(SampleType)

    collected_by = models.ForeignKey(Account, blank=True, null=True)

    def __unicode__(self):
        return '{} sample from {}'.format(self.sample_type, self.collection)

    def get_absolute_url(self):
        return reverse_lazy('lims:envsample-detail', args=[self.id])

    @property
    def in_mixed(self):
        """
        If it is part of more than one EnvironmentalSampleCollection, this will return true.
        """
        return self.environmentalsamplecollection_set.length()

    @property
    def default_collection(self):
        """
        The default auto-created collection of the environmental sample.

        There should only ever be one of these.
        """
        return self.environmentalsamplecollection_set.get(true_collection=False)

class EnvironmentalSampleCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True)
    env_sample = models.ManyToManyField(EnvironmentalSample, blank=True)
    storage = models.OneToOneField(Storage, blank=True, null=True)
    true_collection = models.BooleanField(default=False, help_text="Whether or not this is a 'true' collection of multiple phages, or simply the default collection instance auto-created for an environmental sample")


class Bacteria(models.Model):
    genus = models.CharField(max_length=64)
    species = models.CharField(max_length=64, blank=True)
    strain = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        if self.strain:
            return '{}. {} spp {}'.format(self.genus[0], self.species, self.strain)
        return '{}. {}'.format(self.genus[0], self.species)

    class Meta:
        verbose_name_plural = "bacteria"

    def get_absolute_url(self):
        return reverse_lazy('lims:bacteria-detail', args=[self.id])


class Lysate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    oldid = models.CharField(max_length=64, blank=True)
    isolation = models.DateTimeField(null=True, blank=True)
    storage = models.OneToOneField(Storage, blank=True, null=True)
    host = models.ForeignKey(Bacteria, blank=True)
    env_sample_collection = models.ForeignKey(EnvironmentalSampleCollection, blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('lims:lysate-detail', args=[self.id])


class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_name = models.CharField(max_length=32)
    full_name = models.TextField()
    methods = models.TextField()
    category = models.TextField(blank=True)

    def __unicode__(self):
        return self.short_name


class ExperimentalResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experiment = models.ForeignKey(Experiment)
    result = models.TextField()
    date = models.DateTimeField()
    run_by = models.ForeignKey(Account)
    # result_type = models.IntegerField(choices=EXP_RESULT_TYPES)

    def __unicode__(self):
        return '{} - {}'.format(
            self.experiment.short_name,
            self.result
        )


class PhageDNAPrep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    morphology = models.IntegerField(choices=PHAGE_MORPHOLOGY)

    # These will point to OMERO eventually...
    # tem_image = models.URLField()
    # gel_image = models.URLField()
    # Nanodrop, pico green, other?
    experiments = models.ManyToManyField(ExperimentalResult, blank=True)

    storage = models.OneToOneField(Storage, blank=True, null=True)

    def __unicode__(self):
        return u'%s morphology' % (self.get_morphology_display())


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
        return '{} on {}'.format(self.name, self.date)


class SequencingRunPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pool = models.CharField(max_length=16)
    run = models.ForeignKey(SequencingRun)

    class Meta:
        unique_together = (('pool', 'run'),)

    def __unicode__(self):
        return 'Run "{0.run.name}" Pool {0.pool}'.format(self)

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


class Phage(models.Model):
    primary_name = models.CharField(max_length=64)
    historical_names = models.TextField(blank=True, null=True)  # JSON encoded list of old names
    lysate = models.OneToOneField(Lysate, blank=True, null=True)
    phagednaprep = models.ForeignKey(PhageDNAPrep, blank=True, null=True)
    host = models.ManyToManyField(Bacteria, blank=True)
    owner = models.ForeignKey(Account, blank=True, null=True)
    source = models.ForeignKey(Organisation, blank=True, null=True)
    # notes = models.TextField(blank=True)


class Assembly(models.Model):
    """
    This represents a single assembly run of a single genome's sequencing data
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sequencing_run_pool_item = models.ForeignKey(SequencingRunPoolItem, blank=True, null=True)
    galaxy_dataset = models.URLField()
    notes = models.TextField(blank=True)
    phage = models.ForeignKey(Phage, blank=True, null=True)

    class Meta:
        verbose_name_plural = "assemblies"

    def __unicode__(self):
        return 'Assembly %s' % self.id




def create_default_envsamplecollection(sender, instance, created, **kwargs):
    """Create EnvironmentalSampleCollection for every new EnvironmentalSample."""
    if not created:
        return

    esc = EnvironmentalSampleCollection.objects.create()
    esc.env_sample = [instance]
    esc.save()

signals.post_save.connect(
    create_default_envsamplecollection,
    sender=EnvironmentalSample, weak=False,
    dispatch_uid='models.create_default_envsamplecollection'
)
