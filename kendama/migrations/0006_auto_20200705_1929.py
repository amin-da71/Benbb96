# Generated by Django 2.2.13 on 2020-07-05 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kendama', '0005_auto_20200704_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='combotrick',
            options={'ordering': ('combo', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='combotrick',
            unique_together={('combo', 'trick', 'order')},
        ),
    ]
