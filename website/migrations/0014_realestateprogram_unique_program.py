# Generated by Django 4.2.1 on 2023-06-30 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_remove_realestateprogram_new_date_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='realestateprogram',
            constraint=models.UniqueConstraint(fields=('name', 'address', 'developer'), name='unique_program'),
        ),
    ]
