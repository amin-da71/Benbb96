# Generated by Django 2.1.11 on 2019-08-16 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20190813_1152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='style',
            options={'ordering': ('nom',)},
        ),
    ]
