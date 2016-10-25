from django.core.management.base import BaseCommand, CommandError
from account.models import Account, EmailAddress
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load person table'

    def add_arguments(self, parser):
        parser.add_argument('file', type=file)

    # def personTagMemo(self, tagName):
        # if not hasattr(self, '_tags'):
            # self._tags = {}

        # pt = PersonTag.objects.get_or_create(name=tagName)

        # self._tags[tagName] = pt[0]

        # return self._tags[tagName]

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

            import pprint; pprint.pprint(md)
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

            # pts = []

            # for t in md['tags'].strip().split(';'):
                # if len(t.strip()) == 0:
                    # continue

                # # pt = self.personTagMemo(t.strip())
                # # pts.append(pt)

            # p.tags = pts
            # p.save()
