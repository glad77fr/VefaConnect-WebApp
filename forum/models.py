from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from website.models import RealEstateProgram

# Create your models here.
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True) 
    followed_programs = models.ManyToManyField('website.RealEstateProgram', through='website.FollowedProgram', related_name='followers')
    joined_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True) 
    last_name = models.CharField(max_length=30, blank=True, null=True) 
    gender = models.CharField(max_length=1, null=False, blank=False, choices=GENDER_CHOICES)

    def save(self, *args, **kwargs):
        if not self.photo: # if no photo was provided
            if self.gender == 'M':
                self.photo = 'user_photos/Default_male_profile.jpg'
            elif self.gender == 'F':
                self.photo = 'user_photos/Default_female_profile.jpg'
            else:
                self.photo = 'user_photos/Default_other_profile.jpg'
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username   # remplacer 'name' par le champ qui contient le nom du développeur

class Forum(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ForumTheme(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='themes')

    def __str__(self):
        return self.title

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(ForumTheme, on_delete=models.CASCADE, related_name='posts')
    real_estate_program = models.ForeignKey(RealEstateProgram, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='user_attachments/', blank=True, null=True)

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='user_attachments/', blank=True, null=True)