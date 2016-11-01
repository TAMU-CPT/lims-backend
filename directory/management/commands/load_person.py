from django.core.management.base import BaseCommand
from account.models import EmailAddress
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Load person table'

    def add_arguments(self, parser):
        parser.add_argument('file', type=file)

    def handle(self, *args, **options):
        fn = options['file']

        cols = ['ID', 'f', 'm', 'l', 'netid', 'email', 'fullname', 'nick',
                'init', 'phone', 'tags', 'orcid']
        start_proc = False
        for row in fn:
            if row.startswith('ID\t'):
                start_proc = True
                continue

            if not start_proc:
                continue

            rowData = row.split('\t')

            if len(rowData[1]) == 0:
                continue

            md = {k: v.strip() for (k, v) in zip(cols, rowData)}

            username = md['f'][0] + md['l']
            pu = User.objects.get_or_create(
                username=username.lower(),
                email=md['email'].strip(),
            )
            pu = pu[0]
            print pu
            print md
            p = pu.account
            data = dict(
                timezone='UTC',
                name=md['fullname'].strip(),
                language='en',
                # initials=md.get('initials', '').strip(),
                # emails=md['email'].strip(),
                phone_number=md['phone'].strip(),
                orcid=md['orcid'].strip(),
                netid=md['netid'].strip(),
                original_id=md['ID'].strip(),
            )
            for (k, v) in data.iteritems():
                setattr(p, k, v)

            # Emails
            em = md['email'].strip()
            if len(em) > 0:
                try:
                    EmailAddress.objects.get(email=em)
                except:
                    ea = EmailAddress(
                        user=pu,
                        email=em,
                        verified=False,
                        primary=True
                    )
                    ea.save()
            p.save()
