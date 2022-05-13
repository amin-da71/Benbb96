# Generated by Django 2.1.11 on 2019-10-31 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20190731_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='projet',
            name='logged_only',
            field=models.BooleanField(default=False, help_text="Cochez pour afficher ce projet qu'aux personnes connecté sur le site.", verbose_name='connecté seulement'),
        ),
        migrations.AddField(
            model_name='projet',
            name='staff_only',
            field=models.BooleanField(default=False, help_text="Cochez pour afficher ce projet qu'aux personnes faisant partis du staff.", verbose_name='staff seulement'),
        ),
    ]