# Generated by Django 4.2.1 on 2023-06-30 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_realestateprogram_unique_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestatedeveloper',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
