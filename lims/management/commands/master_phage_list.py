from django.core.management.base import BaseCommand
from django.contrib.auth.models import User  # noqa
from account.models import Account
from directory.models import Organisation
from lims.models import Phage, Lysate, Bacteria, EnvironmentalSample, EnvironmentalSampleCollection
# PhageDNAPrep, SequencingRun, SequencingRunPool, Publication  # noqa
from django.db import transaction
from django.db.models import signals
from lims.models import create_default_phage_for_lysate
import datetime
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

                # morphology names to integers
                morphologies = {
                    "": 0,
                    "podo": 1,
                    "myo": 2,
                    "sipho": 3
                }

                # Account
                account = None
                if row[11]:
                    account = Account.objects.get(name=row[11])

                # EnvironmentalSample
                envsample = None
                if row[11] or row[13] or row[14] or row[15]:  # only create if something is filled out
                    location = None
                    collection_date = None
                    if row[13].strip():
                        locs = [x.strip() for x in row[13].split(',')]
                        location="SRID=4326;POINT (%s %s)" % (locs[1],locs[0])
                    if row[14].strip():
                        collection_date=datetime.datetime.strptime(row[14].strip(), '%Y-%m-%d')
                    envsample, created = EnvironmentalSample.objects.get_or_create(
                        collection=collection_date,
                        location=location,
                        sample_type=row[15].strip().lower(),
                        collected_by=account
                    )

                # EnvironmentalSampleCollection
                envsamplecollection = None
                if envsample:
                    envsamplecollection = envsample.default_collection

                # disconnect autocreate of phage
                signals.post_save.disconnect(
                    create_default_phage_for_lysate,
                    sender=Lysate, weak=False,
                    dispatch_uid='models.create_default_phage_for_lysate'
                )

                # Lysate
                lysate = None
                if row[12].strip() or envsamplecollection is not None or account is not None:
                    lysate = Lysate.objects.create(
                        oldid=row[12].strip(),
                        owner=account,
                        host=None,
                        env_sample_collection=envsamplecollection
                    )

                # create Bacteria objects for each entry in host range
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

                # Organisation
                organisation = ""
                if row[7].strip():
                    organisation, created = Organisation.objects.get_or_create(name=row[7].strip())

                # Phage
                phage, created = Phage.objects.get_or_create(
                    id=int(row[3]),
                    primary_name=row[1].strip(),
                    historical_names=json.dumps([x.strip() for x in row[2].split(';')]),
                    lysate=lysate,
                    owner=organisation,
                    morphology=morphologies[row[33]],
                    ncbi_id=row[53].strip(),
                    refseq_id=row[54].strip()
                )
                if len(hosts):
                    phage.host.add(*hosts)  # manytomany fields have to be added after save
                    phage.save()
