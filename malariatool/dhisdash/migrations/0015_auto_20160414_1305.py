# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0014_auto_20160414_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasetparser',
            name='data_set',
        ),
        migrations.DeleteModel(
            name='DataSetParser',
        ),
    ]
