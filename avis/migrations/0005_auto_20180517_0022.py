# Generated by Django 2.0.4 on 2018-05-16 22:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avis', '0004_auto_20180516_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='telephone',
            field=models.CharField(blank=True, help_text='Indicatif facultatif et sans espaces.', max_length=20, validators=[django.core.validators.RegexValidator('^(0|\\+33|0033)[1-9][0-9]{8}$', "Ce numéro n'est pas valide.")]),
        ),
    ]
