# Generated by Django 4.2.1 on 2023-06-29 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_remove_realestateprogram_start_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realestateprogram',
            name='new_date',
        ),
        migrations.AddField(
            model_name='realestateprogram',
            name='new_end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
