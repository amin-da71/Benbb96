# Generated by Django 2.2.2 on 2019-08-14 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('versus', '0003_auto_20190526_1554'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='partiejoueur',
            unique_together={('partie', 'joueur')},
        ),
    ]
