# Generated by Django 2.1.2 on 2018-10-24 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_testmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='projet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='projet/'),
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='url',
            field=models.TextField(),
        ),
    ]
