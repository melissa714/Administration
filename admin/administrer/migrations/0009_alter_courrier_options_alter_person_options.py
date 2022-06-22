# Generated by Django 4.0.5 on 2022-06-13 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrer', '0008_alter_courrier_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courrier',
            options={'ordering': ['date_ajout'], 'permissions': [('view_courrier_dashboard', 'peut etre vu uniquement par le tableau de bords')]},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['dateE'], 'permissions': [('view_personne_dashboard', 'peut etre vu uniquement par le tableau de bords')]},
        ),
    ]
