# Generated by Django 4.2.1 on 2023-08-03 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_realestateprogram_validated'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnvalidatedRealEstateProgram',
            fields=[
            ],
            options={
                'verbose_name': 'Unvalidated Program',
                'verbose_name_plural': 'Unvalidated Programs',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('website.realestateprogram',),
        ),
    ]
