# Generated by Django 2.1.2 on 2018-11-28 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avis', '0012_auto_20181128_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='avis',
            name='prive',
            field=models.BooleanField(default=False, help_text='Cochez pour cacher cet avis aux utilisateurs non connectés', verbose_name='privé'),
        ),
    ]
