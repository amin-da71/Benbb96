# Generated by Django 2.2.13 on 2020-08-06 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kendama', '0010_auto_20200806_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='ladder',
            name='private',
            field=models.BooleanField(default=False, help_text="Cochez cette case pour que ce ladder ne soit visible qu'à vous.", verbose_name='privé'),
        ),
    ]
