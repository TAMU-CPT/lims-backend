from django.core.management.base import BaseCommand
from django.contrib.auth.models import User  # noqa
from lims.models import Phage, Lysate, Bacteria
# EnvironmentalSampleCollection \
# PhageDNAPrep, SequencingRun, SequencingRunPool, Publication  # noqa
from django.db import transaction
import json
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

                # lysate, created = Lysate.objects.get_or_create(
                # )


                # create bacteria objects for each entry in host range
                hosts = []
                host_range_strains = [x.strip() for x in row[6].split(',')]
                if len(host_range_strains):
                    for h in host_range_strains:
                        bacteria, created = Bacteria.objects.get_or_create(
                            genus=row[5].split()[0],
                            species=row[5].split()[1],
                            strain=h
                        )
                        hosts.append(bacteria)
                else:  # if no strains, just create one bacteria with genus/spcies only
                    bacteria, created = Bacteria.objects.get_or_create(
                        genus=row[5].split()[0],
                        species=row[5].split()[1]
                    )
                    hosts.append(bacteria)

                # phage, created = Phage.objects.get_or_create(
                    # id=int(row[3]),
                    # primary_name=row[1]
                    # historical_names=json.dumps([x.strip() for x in row[2].split(';')]),
                    # lysate="",
                # )
                # phage.save()
                # phage.host.add(hosts) # manytomany fields have to be added after save
