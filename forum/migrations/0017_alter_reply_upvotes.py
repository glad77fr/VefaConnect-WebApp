# Generated by Django 4.2.1 on 2023-10-10 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_reply_upvotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='upvotes',
            field=models.ManyToManyField(related_name='upvoted_responses', to='forum.userprofile'),
        ),
    ]