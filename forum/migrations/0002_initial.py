# Generated by Django 4.2.1 on 2023-05-30 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='followed_programs',
            field=models.ManyToManyField(related_name='followers', through='website.FollowedProgram', to='website.realestateprogram'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reply',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.forumpost'),
        ),
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumtheme',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='themes', to='forum.forum'),
        ),
        migrations.AddField(
            model_name='forumpost',
            name='real_estate_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.realestateprogram'),
        ),
        migrations.AddField(
            model_name='forumpost',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='forum.forumtheme'),
        ),
        migrations.AddField(
            model_name='forumpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
