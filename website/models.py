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

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'address', 'developer'], name='unique_program')
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()  # Normalize the name by converting to lowercase and trimming whitespace
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.pk}')

                # Set default image if not present
        if not self.image:
            default_image_path = os.path.join(settings.BASE_DIR, 'media', 'Default program.jpg')
            self.image.save(
                os.path.basename(default_image_path),
                File(open(default_image_path, 'rb'))
            )

        super().save(*args, **kwargs)

class FollowedProgram(models.Model):
    user_profile = models.ForeignKey('forum.UserProfile', on_delete=models.CASCADE)
    real_estate_program = models.ForeignKey(RealEstateProgram, on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)
    is_owner = models.BooleanField(default=False)
    apartment_lot_reference = models.CharField(max_length=200, blank=True, null=True)
