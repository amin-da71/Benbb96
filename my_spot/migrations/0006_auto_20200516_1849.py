# Generated by Django 2.2.12 on 2020-05-16 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_spot', '0005_auto_20200515_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='spotgroup',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='spottag',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
