from django.core.management import BaseCommand, call_command
from website.models import RealEstateProgram, RealEstateDeveloper, Address, City, Country
from django.db import connection

class Command(BaseCommand):
    help = 'Import all data'

    def handle(self, *args, **options):

        # Delete all existing data
        RealEstateProgram.objects.all().delete()
        RealEstateDeveloper.objects.all().delete()
        Address.objects.all().delete()
        City.objects.all().delete()
        Country.objects.all().delete()

         # Reset autoincrement ID for RealEstateProgram
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='website_realestateprogram';")

        # Import new data
        call_command('import_countries', 'website/data/countries.csv')
        call_command('import_cities', 'website/data/cities.csv')
        call_command('import_developers','website/data/developers.xlsx')
        call_command('import_programs', 'website/data/programs.xlsx')

        self.stdout.write(self.style.SUCCESS('All data imported successfully'))
