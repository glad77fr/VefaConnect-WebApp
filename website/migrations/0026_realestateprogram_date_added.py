# Generated by Django 4.2.1 on 2023-11-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0025_section_image_position_section_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestateprogram',
            name='date_added',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]