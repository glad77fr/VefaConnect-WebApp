from django.db import models
from django.utils.text import slugify

# Create your models here.

class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=30, decimal_places=23,null=True, blank=True)
    longitude = models.DecimalField(max_digits=30, decimal_places=23, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=200, null=True)
    department_code = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

class RealEstateDeveloper(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.pk}') 
            super().save(*args, **kwargs) 

class RealEstateProgram(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    developer = models.ForeignKey(RealEstateDeveloper, on_delete=models.CASCADE, related_name='programs')
    slug = models.SlugField(unique=True, editable=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # On enregistre d'abord l'objet pour obtenir une clé primaire
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.pk}')  # On génère le slug à partir du nom et de la clé primaire
            super().save(*args, **kwargs)  # On enregistre l'objet une deuxième fois pour sauvegarder le slug

class FollowedProgram(models.Model):
    user_profile = models.ForeignKey('forum.UserProfile', on_delete=models.CASCADE)
    real_estate_program = models.ForeignKey(RealEstateProgram, on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)
    is_owner = models.BooleanField(default=False)
    apartment_lot_reference = models.CharField(max_length=200, blank=True, null=True)
