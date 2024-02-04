# Generated by Django 2.2.18 on 2021-03-30 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_auto_20210330_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='LienPlaylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='lien vers la playlist')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('plateforme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='music.Plateforme')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liens', to='music.Playlist')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]