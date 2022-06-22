# Generated by Django 4.0.5 on 2022-06-09 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrer', '0004_alter_person_arme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrer.service', verbose_name='service'),
        ),
        migrations.AlterField(
            model_name='person',
            name='sousdirection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrer.sousdirection'),
        ),
    ]
