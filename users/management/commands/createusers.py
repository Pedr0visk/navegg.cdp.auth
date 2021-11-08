import json

from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Create users to fill database'

    def handle(self, *args, **options):
        json_file = open('postgres_users.json', 'r')
        data = json.loads(json_file.read())

        for item in data:
            accounts_list = []
            if not 'accounts_id' in item:
                accounts_list.append(item['acc_id'])
            else:
                accounts_list = item['accounts_id']

            User.objects.create(
                id=item['id'],
                first_name=item['first_name'],
                last_name=item['last_name'],
                email=item['email'],
                password=item['password'],
                acc_id=int(item['acc_id']),
                accounts_id=accounts_list,
                is_active=True,
                is_staff=False,
                is_superuser=False
            )
        self.stdout.write(self.style.SUCCESS('Users created'))
