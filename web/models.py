from __future__ import unicode_literals
from django.db import models
from directory.models import Person, Organisation


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
),

class ContainerType(models.Model):
    name = models.CharField(max_length=32)

class TubeType(models.Model):
    name = models.CharField(max_length=32)

class SampleType(models.Model):
    name = models.CharField(max_length=32)

class StorageLocation(models.Model):
    # HAS_CPT_HASHID
    # Human readable name that gets written on it
    name = models.CharField(max_length=64)
    # Human readable location
    location = models.CharField(max_length=64)
    # Type of container
    container_type = models.ForeignKey(ContainerType)

class Box(models.Model):
    # HAS_CPT_HASHID
    # Human readable name that gets written on it
    name = models.CharField(max_length=64)
    location = models.ForeignKey(StorageLocation)

class Tube(models.Model):
    # HAS_CPT_HASHID
    tube_type = models.ForeignKey(TubeType)
    box = models.ForeignKey(Box)

class EnvironmentalSample(models.Model):
    # HAS_CPT_HASHID
    collection = models.DateTimeField()
    # location = models.
    # TODO: location
    sample_type = models.ForeignKey(SampleType)
    storage = models.ForeignKey(Tube)

class Bacteria(models.Model):
    genus = models.CharField(max_length=64)
    species = models.CharField(max_length=64)
    strain = models.CharField(max_length=64)

class Lysate(models.Model):
    # HAS_CPT_HASHID
    env_sample = models.ForeignKey(EnvironmentalSample)
    host_lims = models.ManyToManyField(Bacteria)
    storage = models.ForeignKey(Tube)
    oldid = models.CharField(max_length=64)
    isolation = models.DateTimeField()
    owner = models.ForeignKey(Person)
    source = models.ForeignKey(Organisation)

class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_name = models.CharField(max_length=32)
    full_name = models.TextField()
    methods = models.TextField()

class ExperimentalResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experiment = models.ForeignKey(Experiment)
    result = models.TextField()
    result_type = models.IntegerField(choices=EXP_RESULT_TYPES)

class PhageDNAPrep(models.Model):
    # HAS_CPT_HASHID
    # These will point to OMERO eventually...
    # tem_image = models.URLField()
    # gel_image = models.URLField()
    morphology = models.IntegerField(choices=PHAGE_MORPHOLOGY)
    pfge_expected_size = models.FloatField()
    storage = models.ForeignKey(Tube)
    # Nanodrop, pico green, other?
    experiments = models.ManyToManyField(ExperimentalResult)

class SequencingRunPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pool = models.CharField(max_length=16)
    dna_preps = models.ManyToManyField(PhageDNAPrep)

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

class Assembly(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dna_prep = models.ForeignKey(PhageDNAPrep)
    sequencing_run = models.ForeignKey(SequencingRunPool)
    galaxy_dataset = models.URLField()
    notes = models.TextField()
