from website.models import City, Country

# Supprimer toutes les instances de City
City.objects.all().delete()

# Supprimer toutes les instances de Country
Country.objects.all().delete()

