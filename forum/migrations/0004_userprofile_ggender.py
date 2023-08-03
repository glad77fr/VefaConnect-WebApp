# Generated by Django 4.2.1 on 2023-07-31 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_userprofile_first_name_userprofile_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ggender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]