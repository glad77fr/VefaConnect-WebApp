# Generated by Django 4.2.1 on 2023-10-05 08:41

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]