from website.models import City, Country, RealEstateDeveloper

# Supprimer toutes les instances de City
City.objects.all().delete()

# Supprimer toutes les instances de Country
Country.objects.all().delete()

# Supprimer toutes les instance de RealEstateDeveloper
RealEstateDeveloper.objects.all().delete()

