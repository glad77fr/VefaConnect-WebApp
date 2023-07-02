# Generated by Django 4.2.1 on 2023-06-28 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_remove_address_postal_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realestateprogram',
            name='start_date',
        ),
        migrations.AddField(
            model_name='realestateprogram',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='program_images/'),
        ),
        migrations.AddField(
            model_name='realestateprogram',
            name='new_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
