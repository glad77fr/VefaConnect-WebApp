import csv
from django.core.management.base import BaseCommand
from website.models import Country

class Command(BaseCommand):
    help = 'Import data for Country from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                print(row)
                Country.objects.get_or_create(code=row['code'], name=row['name'])
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data for row: {row}'))
