from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from website.models import RealEstateProgram
from django.db.models import Max
import itertools
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.shortcuts import get_object_or_404, redirect
from website.models import FollowedProgram
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    order = models.IntegerField(default=0)
    icon_class = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title
    
    def post_count(self):
        return self.posts.count()

    def get_last_activity_date(self):
        last_post_date = self.posts.aggregate(Max('date_posted'))['date_posted__max']
        last_reply_date = Reply.objects.filter(post__theme=self).aggregate(Max('date_posted'))['date_posted__max']

        if last_post_date and last_reply_date:
            return max(last_post_date, last_reply_date)
        elif last_post_date:
            return last_post_date
        else:
            return last_reply_date
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = original_slug = slugify(self.title)
            for x in itertools.count(1):
                if not ForumTheme.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (original_slug, x)
        super().save(*args, **kwargs)
    
    def post_count(self):
        """Retourne le nombre de posts directement liés à ce thème."""
        return self.posts.count()

    def reply_count(self):
        """Retourne le nombre de réponses à tous les posts de ce thème."""
        return Reply.objects.filter(post__in=self.posts.all()).count()

class ForumPost(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    theme = models.ForeignKey(ForumTheme, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True,null=True)
    real_estate_program = models.ForeignKey(RealEstateProgram, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)


    def last_reply(self):
        last_reply = self.replies.aggregate(Max('date_posted'))['date_posted__max']
        
        if last_reply:
            return last_reply

@receiver(pre_save, sender=ForumPost)
def create_slug_for_post(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title)
        unique_slug = slug
        num = 1
        while ForumPost.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        instance.slug = unique_slug

class Reply(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(UserProfile, related_name="upvoted_responses")

    @property
    def upvote_count(self):
        return self.upvotes.count()

