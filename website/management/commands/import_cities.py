import csv
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from website.models import City, Country

class Command(BaseCommand):
    help = 'Import data for City from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        with open(csv_file, 'r',encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                print(row)
                # Try to convert latitude and longitude to decimal, if fails, set to None
                try:
                    latitude = Decimal(row['latitude'])
                except (ValueError, TypeError, InvalidOperation):
                    latitude = None
                
                try:
                    longitude = Decimal(row['longitude'])
                except (ValueError, TypeError, InvalidOperation):
                    longitude = None

                city = City.objects.create(
                    name=row['name'],
                    country=Country.objects.get(code=row['country']),
                    postal_code=row['postal_code'],
                    latitude=latitude,
                    longitude=longitude,
                    department=row['department'],
                    region=row['region'],
                    department_code = row['department_code']
                )
                self.stdout.write(self.style.SUCCESS(f'Successly imported data for city: {city}'))
