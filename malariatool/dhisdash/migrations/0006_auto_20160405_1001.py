# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0005_auto_20160401_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSetParser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.IntegerField()),
                ('status', models.IntegerField()),
                ('data_set', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dhisdash.DataSet', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='datavalue',
            name='data_set_parser',
            field=models.ForeignKey(default=0, to='dhisdash.DataSetParser'),
            preserve_default=False,
        ),
    ]
