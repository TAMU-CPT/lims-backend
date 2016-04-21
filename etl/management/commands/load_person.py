from django.core.management.base import BaseCommand, CommandError
from directory.models import Person, PersonTag

class Command(BaseCommand):
    help = 'Load person table'

    def add_arguments(self, parser):
        parser.add_argument('file', type=file)

    def personTagMemo(self, tagName):
        if not hasattr(self, '_tags'):
            self._tags = {}

        pt = PersonTag.objects.get_or_create(name=tagName)

        self._tags[tagName] = pt[0]

        return self._tags[tagName]

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

            p = Person.objects.get_or_create(
                name=md['fullname'].strip(),
                initials=md['initials'].strip(),
                emails=md['email'].strip(),
                phone_number=md['phone'].strip(),
                orcid=md['orcid'].strip(),
                netid=md['netid'].strip(),
                original_id=md['ID'].strip()
            )
            p = p[0]

            pts = []

            for t in md['tags'].strip().split(';'):
                if len(t.strip()) == 0:
                    continue

                pt = self.personTagMemo(t.strip())
                pts.append(pt)

            p.tags = pts
            p.save()
            print p
