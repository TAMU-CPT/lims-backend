from django.core.management.base import BaseCommand
from lims.models import Phage, EnvironmentalSample, \
    EnvironmentalSampleCollection, Bacteria, Lysate, \
    PhageDNAPrep, SequencingRun, SequencingRunPool, Publication
from django.contrib.auth.models import User
from django.db import transaction
import csv

class Command(BaseCommand):
    help = 'makes objects from information in Master Phage List spreadsheet'

    def add_arguments(self, parser):
        parser.add_argument('master_phage_list', type=str)

    @transaction.atomic
    def handle(self, *args, **options):

        with open(options['master_phage_list'], 'rU') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for i, row in enumerate(csvreader):
                if i == 0 or i == 1 or not row[1]:
                    continue
