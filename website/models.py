from django.db import models
from django.utils.text import slugify
import os
from django.conf import settings
from django.core.files import File
from ckeditor_uploader.fields import RichTextUploadingField
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import logging
import uuid
import requests


logger = logging.getLogger(__name__)

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
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"
    
    def save(self, *args, **kwargs):
        transaction_id = uuid.uuid4()
        logger.info(f"[{transaction_id}] Starting the save process for Address")
        if not self.latitude or not self.longitude:
            geolocator = Nominatim(user_agent="VefaConnect")  # Assurez-vous d'utiliser un user_agent unique
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            address_str = f"{self.street}, {self.city.name}, {self.country.name}"
            logger.info(f"[{transaction_id}] Attempting to geocode this address: {address_str}")
            try:
                location = geocode(address_str)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                    logger.info(f"[{transaction_id}] Geocoded to: Lat {self.latitude}, Lon {self.longitude}")
                else:
                    logger.warning(f"[{transaction_id}] Geocoding failed, no location found.")
            except Exception as e:
                logger.error(f"[{transaction_id}] An error occurred during geocoding: {e}")

        super().save(*args, **kwargs)  # Call the "real" save() method.
        logger.info(f"[{transaction_id}] Save process completed for Address")

class RealEstateDeveloper(models.Model):
    name = models.CharField(max_length=200, unique=True) 
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.name  # remplacer 'name' par le champ qui contient le nom du développeur

    def save(self, *args, **kwargs):
        if not self.pk:  # If the object has not been saved yet
            super(RealEstateDeveloper, self).save(*args, **kwargs)  # Save it to get an ID
            self.slug = slugify(f'{self.name}-{self.pk}')  # Now we can generate the slug
        else:
            if not self.slug:  # In case the object was saved before but without a slug
                self.slug = slugify(f'{self.name}-{self.pk}')
        super(RealEstateDeveloper, self).save(*args, **kwargs)  # Save the object again, with the slug


class RealEstateProgram(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    developer = models.ForeignKey(RealEstateDeveloper, on_delete=models.CASCADE, related_name='programs')
    slug = models.SlugField(unique=True, editable=False)
    end_date = models.DateField(null=True, blank=True)
    new_end_date = models.DateField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='program_images/', null=True, blank=True)
    validated = models.BooleanField(default=False, null=False)
    date_added = models.DateField(null=True, blank=True, auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'address', 'developer'], name='unique_program')
        ]
    def __str__(self):
            return self.name
    
    def save(self, *args, **kwargs):
            self.name = self.name.strip().lower()  # Normalize the name by converting to lowercase and trimming whitespace

            # First, save the model so it has a pk if it's a new record
            super().save(*args, **kwargs)

            # Then, update the slug using the name and pk
            if not self.slug:
                generated_slug = slugify(f'{self.name}-{self.pk}')
                self.slug = generated_slug

                # Check for slug uniqueness
                unique_slug = generated_slug
                num = 1

                while RealEstateProgram.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                    unique_slug = f'{generated_slug}-{num}'
                    num += 1

                self.slug = unique_slug

            # Set default image if not present
            if not self.image:
                default_image_path = os.path.join(settings.BASE_DIR, 'media', 'program_images/Default_program.jpg')
                self.image.save(
                    os.path.basename(default_image_path),
                    File(open(default_image_path, 'rb'))
                )

            # Save the model again to record any changes we've made
            super().save(*args, **kwargs)


class UnvalidatedRealEstateProgram(RealEstateProgram):
    class Meta:
        proxy = True
        verbose_name = 'Unvalidated Program'
        verbose_name_plural = 'Unvalidated Programs'


class FollowedProgram(models.Model):
    user_profile = models.ForeignKey('forum.UserProfile', on_delete=models.CASCADE)
    real_estate_program = models.ForeignKey(RealEstateProgram, on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)
    is_owner = models.BooleanField(default=False)
    apartment_lot_reference = models.CharField(max_length=200, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Optionnel

    def save(self, *args, **kwargs):
        # Si le slug n'est pas défini
        if not self.slug:
            # Utilisez slugify pour créer un slug à partir du nom
            # Pour éviter des doublons, ajoutez un compteur si nécessaire
            potential_slug = slugify(self.name)
            counter = 1
            while Category.objects.filter(slug=potential_slug).exists():
                potential_slug = "{}-{}".format(slugify(self.name), counter)
                counter += 1
            self.slug = potential_slug
        super(Category, self).save(*args, **kwargs) 

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    associated_articles = models.ManyToManyField('self', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
            return self.title

    def save(self, *args, **kwargs):
        # Si le slug n'est pas défini
        if not self.slug:
            # Utilisez slugify pour créer un slug à partir du titre
            # Pour éviter des doublons, ajoutez un compteur si nécessaire
            potential_slug = slugify(self.title)
            counter = 1
            while Article.objects.filter(slug=potential_slug).exists():
                potential_slug = "{}-{}".format(slugify(self.title), counter)
                counter += 1
            self.slug = potential_slug
        super(Article, self).save(*args, **kwargs)

class Section(models.Model):
    ARTICLE_SECTION_CHOICES = (
        ('text', 'Texte'),
        ('image', 'Image'),
        # Ajoutez d'autres types selon vos besoins
    )
    IMAGE_POSITION_CHOICES = (
        ('title', 'Image de titre'),
        ('left', 'Image à gauche'),
        ('right', 'Image à droite'),
    )
    type = models.CharField(max_length=50, choices=ARTICLE_SECTION_CHOICES)
    image_position = models.CharField(max_length=50, choices=IMAGE_POSITION_CHOICES, blank=True, null=True, default='left') # Nouveau champ
    order = models.PositiveIntegerField(default=0) # Nouveau champ
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to='articles/sections/', blank=True, null=True)
    caption = models.TextField(blank=True)        # Légende pour l'image
    alt_text = models.CharField(max_length=255, blank=True)   # Texte alternatif pour l'image
    

