from __future__ import unicode_literals
import uuid
from django.db import models
from directory.models import Organisation
from account.models import Account
from django.core.urlresolvers import reverse_lazy


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
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class TubeType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class SampleType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class StorageLocation(models.Model):
    # HAS_CPT_HASHID
    # Human readable name that gets written on it
    name = models.CharField(max_length=64)
    # Human readable location
    location = models.CharField(max_length=64)
    # Type of container
    container_type = models.ForeignKey(ContainerType)

    def __str__(self):
        return '{} in {}'.format(self.name, self.location)

    def get_absolute_url(self):
        return reverse_lazy('lims:storage-location-detail', args=[self.id])

class Box(models.Model):
    # HAS_CPT_HASHID
    # Human readable name that gets written on it
    name = models.CharField(max_length=64, help_text="The name which is written on the outside of the box.")
    location = models.ForeignKey(StorageLocation)

    def __str__(self):
        return '{} in {}'.format(self.name, self.location)

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
    # DOES NOT HAVE CPT_HASHID. Inherits the hashid of whoever is
    #m referring to it.
    # Human readable name that gets written on it
    name = models.CharField(max_length=64)
    box = models.ForeignKey(Box)
    type = models.ForeignKey(TubeType)

    def __str__(self):
        return '{} in {}'.format(self.name, self.box)

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

class EnvironmentalSample(models.Model):
    # HAS_CPT_HASHID
    collection = models.DateTimeField()
    # location = models.
    # TODO: location
    sample_type = models.ForeignKey(SampleType)

    # Tube Storage
    tube = models.OneToOneField(Tube)

    def __str__(self):
        return '{} sample from {}'.format(self.sample_type, self.collection)

class Bacteria(models.Model):
    genus = models.CharField(max_length=64)
    species = models.CharField(max_length=64, blank=True)
    strain = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return '{}. {} spp {}'.format(self.genus[0], self.species, self.strain)

    class Meta:
        verbose_name_plural = "bacteria"

class Lysate(models.Model):
    # HAS_CPT_HASHID
    env_sample = models.ForeignKey(EnvironmentalSample)
    host_lims = models.ManyToManyField(Bacteria, blank=True)
    oldid = models.CharField(max_length=64, blank=True)
    isolation = models.DateTimeField(blank=True)
    owner = models.ForeignKey(Account, blank=True, null=True)
    source = models.ForeignKey(Organisation, blank=True, null=True)

    # Tube Storage
    tube = models.OneToOneField(Tube)

    def __str__(self):
        return 'Lysate from {}'.format(self.env_sample)

class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_name = models.CharField(max_length=32)
    full_name = models.TextField()
    methods = models.TextField()

    def __str__(self):
        return self.short_name

class ExperimentalResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experiment = models.ForeignKey(Experiment)
    result = models.TextField()
    date = models.DateTimeField()
    run_by = models.ForeignKey(Account)
    # result_type = models.IntegerField(choices=EXP_RESULT_TYPES)

    def __str__(self):
        return '{} - {}'.format(
                self.experiment.short_name,
                self.result)

class PhageDNAPrep(models.Model):
    # HAS_CPT_HASHID
    # These will point to OMERO eventually...
    # tem_image = models.URLField()
    # gel_image = models.URLField()
    lysate = models.ForeignKey(Lysate)

    morphology = models.IntegerField(choices=PHAGE_MORPHOLOGY)
    pfge_expected_size = models.FloatField(blank=True)
    # Nanodrop, pico green, other?
    experiments = models.ManyToManyField(ExperimentalResult, blank=True)

    # Tube Storage
    tube = models.OneToOneField(Tube)

    def __str__(self):
        return '{} kb {}'.format(int(self.pfge_expected_size / 1000), self.get_morphology_display())

class SequencingRunPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pool = models.CharField(max_length=16)
    dna_preps = models.ManyToManyField(PhageDNAPrep)

    def __str__(self):
        return 'Pool {}'.format(self.pool)

class SequencingRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pools = models.ManyToManyField(SequencingRunPool)
    galaxy_history = models.URLField()
    name = models.TextField()
    date = models.DateField()
    # Illumina, miseq, etc need to be in experiments
    methods = models.ForeignKey(Experiment)
    bioanalyzer_qc = models.TextField()
    run_prep_spreadsheet = models.URLField()

    def __str__(self):
        return '{} on {}'.format(self.name, self.date)

class Assembly(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dna_prep = models.ForeignKey(PhageDNAPrep)
    sequencing_run = models.ForeignKey(SequencingRunPool)
    galaxy_dataset = models.URLField()
    notes = models.TextField()

    class Meta:
        verbose_name_plural = "assemblies"
