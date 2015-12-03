# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_document_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='areas_of_operations',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ip',
            name='implementation_period',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ip',
            name='objectives',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ip',
            name='overview',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='end_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(max_length=50, choices=[(b'Policy', b'Policy'), (b'Guideline', b'Guideline'), (b'Manual', b'Manual')]),
        ),
    ]
