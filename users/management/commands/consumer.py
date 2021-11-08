import json

from django.core.management.base import BaseCommand
from users.models import User
from users.consumer import main


class Command(BaseCommand):
    help = 'Start Kafka consumer'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting consumer...'))
        main()
