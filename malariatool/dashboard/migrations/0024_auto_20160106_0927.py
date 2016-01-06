# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_auto_20151216_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(max_length=150, choices=[(b'training', b'Training'), (b'supervision', b'Supervision'), (b'bcc', b'BCC'), (b'new_distribution', b'New Distribution'), (b'iptp', b'IPTp'), (b'irs', b'IRS')]),
        ),
    ]
