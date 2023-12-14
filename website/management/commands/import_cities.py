import csv
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from website.models import City, Country, State

class Command(BaseCommand):
    help = 'Import data for City from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        with open(csv_file, 'r',encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
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
                
                # Get or create the corresponding state
                state, created = State.objects.get_or_create(
                    code=row['department_number'],
                    defaults={'name': row['department_name'], 'country': Country.objects.get(code="FR")}
                )
                
                # Now use the state instance to create the city
                city, created = City.objects.get_or_create(
                    name=row['label'].capitalize(),
                    defaults={
                        'country': Country.objects.get(code="FR"),
                        'postal_code': row['zip_code'],
                        'latitude': latitude,
                        'longitude': longitude,
                        'department_code': row['department_number'],
                        'state': state
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully imported data for city: {city}'))
                else:
                    self.stdout.write(self.style.WARNING(f'City already exists: {city}'))
