# Generated by Django 2.1.11 on 2019-10-28 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avis', '0014_auto_20181224_1918'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produit',
            options={'ordering': ('nom',)},
        ),
        migrations.AlterModelOptions(
            name='structure',
            options={'ordering': ('nom',)},
        ),
        migrations.AlterField(
            model_name='structure',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
