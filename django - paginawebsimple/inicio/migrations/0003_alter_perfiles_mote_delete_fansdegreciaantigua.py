# Generated by Django 5.0.6 on 2024-07-02 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0002_rename_fan_perfiles_mote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiles',
            name='mote',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='FansDeGreciaAntigua',
        ),
    ]
