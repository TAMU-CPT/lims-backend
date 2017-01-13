from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from account.models import Account
from directory.models import Organisation
from lims.models import Phage, Lysate, Bacteria, EnvironmentalSample, EnvironmentalSampleCollection, \
    PhageDNAPrep, ExperimentalResult, SequencingRun, SequencingRunPool, \
    SequencingRunPoolItem, Publication, Assembly, AnnotationRecord


class Command(BaseCommand):
    help = 'deletes phages, envsamples, organisations, lysates, bacteria from db'

    def handle(self, *args, **options):
        Phage.objects.all().delete()
        EnvironmentalSample.objects.all().delete()
        EnvironmentalSampleCollection.objects.all().delete()
        Organisation.objects.all().delete()
        Lysate.objects.all().delete()
        Bacteria.objects.all().delete()
        PhageDNAPrep.objects.all().delete()
        SequencingRun.objects.all().delete()
        SequencingRunPool.objects.all().delete()
        SequencingRunPoolItem.objects.all().delete()
        Publication.objects.all().delete()
        Assembly.objects.all().delete()
        AnnotationRecord.objects.all().delete()
