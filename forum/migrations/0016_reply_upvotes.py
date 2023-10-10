# Generated by Django 4.2.1 on 2023-10-10 15:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0015_forumpost_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='upvotes',
            field=models.ManyToManyField(related_name='upvoted_responses', to=settings.AUTH_USER_MODEL),
        ),
    ]
