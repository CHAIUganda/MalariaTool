# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20151202_0534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='task',
            name='target_acutal_per_quarter',
        ),
        migrations.RemoveField(
            model_name='task',
            name='target_output_per_quarter',
        ),
        migrations.AddField(
            model_name='task',
            name='ip',
            field=models.ForeignKey(related_name='tasks', default=None, to='dashboard.IP'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.CharField(default=None, max_length=150, choices=[(b'training', b'Training'), (b'supervision', b'Supervision'), (b'bcc', b'BCC'), (b'net_distribution', b'New Distribution'), (b'iptp', b'IPTp'), (b'irs', b'IRS')]),
            preserve_default=False,
        ),
    ]
