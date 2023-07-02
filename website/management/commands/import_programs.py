import pandas as pd
from django.core.management.base import BaseCommand
from website.models import RealEstateProgram, RealEstateDeveloper, Address, City
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Command to import real estate programs from .xlsx file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Indicates the path to the .xlsx file")

    def handle(self, *args, **options):
        file_path = options['file_path']

        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            program_name = row['Programme']
            description = row['Description']
            developer_name = row['Promoteur']
            street = row['RUE']
            postal_code = row['Code postal']
            end_date = pd.to_datetime(row['Date de fin'])


            # Get or create the developer object
            try:
                developer = RealEstateDeveloper.objects.get(name__iexact=developer_name)
            except RealEstateDeveloper.DoesNotExist:
                developer = RealEstateDeveloper.objects.create(name=developer_name)

            # Try to get city object
            try:
                city = City.objects.get(postal_code=postal_code)
            except City.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'No city found with postal code: {postal_code}'))

            # Create or get the address object
            address, created = Address.objects.get_or_create(street=street, city=city, country=city.country)

           ## Create or get the real estate program
            try:
                program, created = RealEstateProgram.objects.get_or_create(
                    name=program_name.strip().lower(),
                    developer=developer,
                    address=address,
                    defaults={
                        'description': description,
                        'end_date': end_date,
                    }
                )
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'IntegrityError for program "{program_name}", developer "{developer_name}", address "{street}, {postal_code}"'))
                raise e  # raise the error again to see the full traceback and stop the command


        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
