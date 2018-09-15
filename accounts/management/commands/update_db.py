from django.core.management.base import BaseCommand
from accounts.models import Account, AccountExtra


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = Account.objects.all()
        for user in users:
            AccountExtra.objects.create(account=user)
