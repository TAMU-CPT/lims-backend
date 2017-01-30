from django.core.management.base import BaseCommand
from account.models import EmailAddress
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Load person table'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        u = User.objects.get(email=options['email'])
        u.is_admin = True
        u.is_staff = True
        u.is_superuser = True
        u.save()
