import csv
from django.core.management.base import BaseCommand
from myapp.models import RealEstateDeveloper

class Command(BaseCommand):
    help = 'Import data for RealEstateDeveloper from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                developer = RealEstateDeveloper.objects.create(name=row['developer_name'], description=row['developer_description'])
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data for developer: {developer}'))
