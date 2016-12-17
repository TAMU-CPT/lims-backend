from django.core.management.base import BaseCommand
from lims.models import Phage
from account.models import Account
import names
import random


class Command(BaseCommand):
    help = 'Generate some env samples'

    def handle(self, *args, **options):
        accounts = Account.objects.all()
        for i in range(30):
            Phage.objects.create(
                primary_name=names.get_first_name(gender='female'),
                historical_names=names.get_first_name(gender='female'),
                owner=random.choice(accounts)
            )
