from account.models import Account, EmailAddress

Account.objects.all().delete()
EmailAddress.objects.all().delete()
