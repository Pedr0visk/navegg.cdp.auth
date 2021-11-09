from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Update account list ids'

    def handle(self, *args, **options):
        accounts_id_list = [1, 78498]
        User.objects.all().update(accounts_id=accounts_id_list)

        self.stdout.write(self.style.SUCCESS('Users updated'))
