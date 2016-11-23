from django.core.management.base import BaseCommand
from random import randint
from lims.models import EnvironmentalSample, Tube, Box, TubeType, SampleType
import datetime



class Command(BaseCommand):
    help = 'Generate some env samples'

    def handle(self, *args, **options):
        for i in range(10):
            t, _ = Tube.objects.get_or_create(
                name="p%s" % randint(1,1000),
                box=Box.objects.get(),
                type=TubeType.objects.get(),
            )

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
                tube=t,
                sample_type=SampleType.objects.get(name="water")
            )
            e = EnvironmentalSample(**d)
            e.save()


