from django.core.management.base import BaseCommand
from account.models import Account
from directory.models import Organisation
from lims.models import Phage, Lysate, Bacteria, EnvironmentalSample, \
    PhageDNAPrep, Experiment, ExperimentalResult, SequencingRun, \
    SequencingRunPool, SequencingRunPoolItem, Assembly, Publication, \
    AnnotationRecord
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

    @transaction.atomic  # noqa
    def handle(self, *args, **options):

        with open(options['master_phage_list'], 'rU') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for i, row in enumerate(csvreader):
                if i == 0 or i == 1 or not row[1]:
                    continue
                print(row[1])

                # morphology names/qualifiers to integers
                morphologies = {
                    "": 0,
                    "podo": 1,
                    "myo": 2,
                    "sipho": 3
                }
                morphology_qualifiers = {
                    "": 0,
                    "prolate": 1,
                    "isometric": 2
                }

                # publication qualifiers to integers
                pub_qualifiers = {
                    "": 0,
                    "unpublished": 1,
                    "manuscript in preparation": 2,
                    "in press": 3,
                    "published": 4
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
                        location = "SRID=4326;POINT (%s %s)" % (locs[1], locs[0])
                    if row[14].strip():
                        collection_date = datetime.datetime.strptime(row[14].strip(), '%Y-%m-%d')
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
                host_range = [x.strip() for x in row[6].split(',')]
                bacteria=None
                if len(host_range[0]):
                    if row[5].startswith('Caul'):
                        for h in host_range:
                            bacteria, created = Bacteria.objects.get_or_create(
                                genus=row[5].strip().split()[0],
                                species=row[5].strip().split()[1],
                                strain=h
                            )
                            hosts.append(bacteria)
                    else:
                        bacteria, created = Bacteria.objects.get_or_create(
                            genus=row[5].strip().split()[0],
                            species=row[5].strip().split()[1],
                            strain=None
                        )
                        hosts.append(bacteria)
                        for h in host_range:
                            bacteria, created = Bacteria.objects.get_or_create(
                                genus=h.split()[0],
                                species=h.split()[1],
                                strain=None
                            )
                            hosts.append(bacteria)
                else:  # if no strains, just create one bacteria with genus/spcies or just genus only
                    if len(row[5].split()) == 3:
                        bacteria, created = Bacteria.objects.get_or_create(
                            genus=row[5].strip().split()[0],
                            species=row[5].strip().split()[1],
                            strain=row[5].strip().split()[2]
                        )
                        hosts.append(bacteria)
                    elif len(row[5].split()) == 2:
                        bacteria, created = Bacteria.objects.get_or_create(
                            genus=row[5].strip().split()[0],
                            species=row[5].strip().split()[1],
                            strain=None
                        )
                        hosts.append(bacteria)
                    elif len(row[5].split()) == 1:
                        bacteria, created = Bacteria.objects.get_or_create(
                            genus=row[5].strip(),
                            species=None,
                            strain=None
                        )
                        hosts.append(bacteria)

                # Organisation
                organisation = None
                if row[7].strip():
                    organisation, created = Organisation.objects.get_or_create(name=row[7].strip())

                # Phage
                can_be_annotated = False
                if row[43] == 'TRUE':
                    can_be_annotated = True
                needs_resequencing = False
                if row[21] == 'TRUE':
                    needs_resequencing = True
                head_size = None
                if row[32].strip():
                    head_size = float(row[32].strip())

                closure_exp_result = None
                if row[36].strip():
                    closure_exp = Experiment.objects.get(short_name='Closure')
                    closure_exp_result = ExperimentalResult.objects.create(
                        experiment=closure_exp,
                        result=row[36]
                    )
                end_exp_result = None
                if row[39].strip():
                    end_exp = Experiment.objects.get(short_name='End determination')
                    end_exp_result = ExperimentalResult.objects.create(
                        experiment=end_exp,
                        result=row[39]
                    )

                phage, created = Phage.objects.get_or_create(
                    id=int(row[3]),
                    primary_name=row[1].strip(),
                    historical_names=json.dumps([x.strip() for x in row[2].split(';')]),
                    lysate=lysate,
                    owner=organisation,
                    morphology=morphologies[row[33]],
                    morphology_qualifier=morphology_qualifiers[row[34]],
                    ncbi_id=row[53].strip(),
                    refseq_id=row[54].strip(),
                    needs_resequencing=needs_resequencing,
                    end_info=row[35].strip(),
                    head_size=head_size,
                    can_be_annotated=can_be_annotated,
                    closure=closure_exp_result,
                    end_determination=end_exp_result
                )
                if len(hosts):
                    phage.host.add(*hosts)  # manytomany fields have to be added after save
                    phage.save()

                # PhageDNAPrep
                exp_result_pfge = None
                if row[18].strip():
                    pfge_experiment = Experiment.objects.get(short_name='PFGE')
                    exp_result_pfge = ExperimentalResult.objects.create(
                        experiment=pfge_experiment,
                        result=row[18].strip()
                    )
                phagednaprep = PhageDNAPrep.objects.create(
                    pfge=exp_result_pfge,
                    phage=phage
                )

                # Sequencing
                seq_experiment = None
                if row[20].strip():
                    if row[20].strip().startswith('MiSeq'):
                        expname = row[20].strip()[:12]
                    else:
                        expname = row[20].strip()
                    seq_experiment, created = Experiment.objects.get_or_create(
                        short_name=expname,
                        full_name=expname,
                        methods=row[20]
                    )
                seq_run_date = None
                if row[19].strip():
                    if '/' in row[19]:
                        seq_run_date = datetime.datetime.strptime(row[19].strip(), '%Y/%m')
                    else:
                        seq_run_date = datetime.datetime.strptime(row[19].strip(), '%Y')
                sequencingrun, created = SequencingRun.objects.get_or_create(
                    name=row[19].strip(),
                    date=seq_run_date,
                    method=seq_experiment,
                    finalized=True
                )
                sequencingrunpool, created = SequencingRunPool.objects.get_or_create(
                    pool=row[24].strip(),
                    run=sequencingrun
                )
                sequencingrunpoolitem = SequencingRunPoolItem.objects.create(
                    pool=sequencingrunpool,
                    dna_prep=phagednaprep
                )

                # Assembly
                if row[30] == 'TRUE':
                    complete = True
                elif row[30] == 'FALSE':
                    complete = False
                else:
                    complete = None
                contig_length = None
                if row[28].strip():
                    contig_length = row[28].strip()
                assembly = Assembly.objects.create(
                    sequence_id=row[27],
                    sequencing_run_pool_item=sequencingrunpoolitem,
                    contig_length=contig_length,
                    contig_name=row[25],
                    complete=complete
                )

                # Publication
                publication, created = Publication.objects.get_or_create(
                    doi=row[50].strip(),
                    status=pub_qualifiers[row[49]]
                )
                publication.phages.add(phage)  # manytomany fields have to be added after save
                publication.save()

                # AnnotationRecord
                annotation_notes = row[47]+'\n'+row[48]
                if row[46].strip():
                    annotation_year = datetime.datetime.strptime(row[46].strip(), '%Y')
                annotator = None
                if row[45] and not row[45].endswith('?'):
                    annotator = Account.objects.get(name=row[45])
                AnnotationRecord.objects.create(
                    assembly=assembly,
                    notes=annotation_notes,
                    annotator=annotator,
                    date=annotation_year
                )
