# Generated by Django 2.1.11 on 2019-08-20 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('versus', '0004_auto_20190814_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joueur',
            name='profil',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Profil'),
        ),
    ]
