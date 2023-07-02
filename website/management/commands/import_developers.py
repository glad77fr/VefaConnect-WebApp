import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from website.models import RealEstateDeveloper  # Remplacez 'yourapp' par le nom de votre application

class Command(BaseCommand):
    help = 'Importe des développeurs immobiliers à partir d\'un fichier Excel'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Chemin du fichier Excel à importer")

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            raise CommandError(f'Erreur lors de la lecture du fichier Excel : {e}')

        for index, row in df.iterrows():
            dev = RealEstateDeveloper(
                name=row['Promoteur'],
                description=row['Description']
            )
            dev.save()

        self.stdout.write(self.style.SUCCESS(f"Importation réussie depuis le fichier {file_path}"))
