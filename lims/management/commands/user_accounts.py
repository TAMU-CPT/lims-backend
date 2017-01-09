from django.core.management.base import BaseCommand
from account.models import Account
from django.contrib.auth.models import User
import csv
from django.db import transaction

class Command(BaseCommand):
    help = 'makes accounts for rows in CPT person ID sheet'

    def add_arguments(self, parser):
        parser.add_argument('account_file', type=str)

    @transaction.atomic
    def handle(self, *args, **options):

        with open(options['account_file'], 'rU') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for i, row in enumerate(csvreader):
                if row[1] == 'Eleni' or i == 0 or i == 1 or i == 2 or not row[1]:
                    continue

                if row[5]:
                    user, created = User.objects.get_or_create(
                        username=row[5],
                        email=row[5]
                    )
                else:
                    user, created = User.objects.get_or_create(
                        username=row[6].replace(' ', '')
                    )

                account, created = Account.objects.get_or_create(
                    user=user,
                    netid=row[4],
                    name=row[6],
                    nickname=row[7],
                    initials=row[8],
                    phone_number=row[9],
                    orcid=row[11],
                )
