# Generated by Django 4.0.5 on 2022-06-13 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20220613_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Photo de profil'),
        ),
    ]
