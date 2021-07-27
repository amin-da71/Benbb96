# Generated by Django 2.1.2 on 2018-11-28 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avis', '0006_auto_20181128_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='plat',
            old_name='restaurant',
            new_name='structure',
        ),
        migrations.AlterField(
            model_name='structure',
            name='informations',
            field=models.TextField(blank=True, help_text='Informations utiles et relatives à la structure'),
        ),
        migrations.AddField(
            model_name='structure',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='avis.TypeStructure', verbose_name='type de la structure'),
            preserve_default=False,
        ),
    ]