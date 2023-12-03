import csv
from django.core.management.base import BaseCommand
from website.models import State, Country

class Command(BaseCommand):
    help = 'Import states from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_filename = kwargs['csv_filename']
        
        # Assurez-vous que le pays France est présent dans la base de données
        france, _ = Country.objects.get_or_create(code='FR', defaults={'name': 'France'})
        
        with open(csv_filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                State.objects.get_or_create(
                    name=row['nom_departement'],
                    code=row['code_departement'],
                    country=france
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported states'))
