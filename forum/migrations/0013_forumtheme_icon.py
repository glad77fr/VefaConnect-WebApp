# Generated by Django 4.2.1 on 2023-08-18 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_alter_reply_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumtheme',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='forum_icons/'),
        ),
    ]
