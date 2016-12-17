from django.core.management.base import BaseCommand
from random import randint, choice
from lims.models import EnvironmentalSample, SampleType, EnvironmentalSampleRelation, EnvironmentalSampleCollection
from account.models import Account
import datetime

class Command(BaseCommand):
    help = 'Generate some env samples'

    def handle(self, *args, **options):
        users = Account.objects.all()

        for i in range(10):
            d = dict(
                description='autogen',
                collection=datetime.datetime(
                    year=randint(2005,2025),
                    month=randint(1,12),
                    day=randint(1,28),
                    hour=randint(0,23),
                    minute=randint(0,60)
                ),
                location="SRID=4326;POINT (%s %s)" % (randint(-30,30), randint(-30,30)),
                sample_type=SampleType.objects.get_or_create(name=choice(['water', 'dirt', 'ice', 'sewage']))[0],
                collected_by=choice(users),
            )
            e = EnvironmentalSample(**d)
            e.save()

        env_samples = EnvironmentalSample.objects.all()
        for _ in range(4):
            # create a collection
            esc = EnvironmentalSampleCollection.objects.create(description='autogen', true_collection=True)
            # Pick some random samples
            for i in range(randint(2,5)):
                esr = EnvironmentalSampleRelation.objects.create(
                    es=choice(env_samples),
                    esc=esc,
                    true_collection=True
                )
