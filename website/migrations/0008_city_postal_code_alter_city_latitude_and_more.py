# Generated by Django 4.2.1 on 2023-06-20 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_remove_city_postal_code_alter_city_department_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='postal_code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='latitude',
            field=models.DecimalField(decimal_places=15, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='longitude',
            field=models.DecimalField(decimal_places=15, max_digits=20, null=True),
        ),
    ]
