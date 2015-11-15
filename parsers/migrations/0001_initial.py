# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OnedenAliment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('calories', models.DecimalField(max_digits=7, decimal_places=2)),
                ('proteins', models.DecimalField(max_digits=7, decimal_places=2)),
                ('fats', models.DecimalField(max_digits=7, decimal_places=2)),
                ('carbohydrates', models.DecimalField(max_digits=7, decimal_places=2)),
                ('fibres', models.DecimalField(max_digits=7, decimal_places=2)),
                ('unit_quantity', models.DecimalField(max_digits=7, decimal_places=2)),
                ('additional', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OnedenCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='onedenaliment',
            name='category',
            field=models.ForeignKey(to='parsers.OnedenCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='onedenaliment',
            unique_together=set([('category', 'name')]),
        ),
    ]
