# Generated by Django 2.1.2 on 2018-10-24 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avis', '0004_auto_20181024_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='photo',
            field=models.TextField(blank=True, null=True),
        ),
    ]