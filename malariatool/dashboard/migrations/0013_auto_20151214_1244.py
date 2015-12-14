# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20151210_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=model_utils.fields.StatusField(default=b'not_started', max_length=100, no_check_for_status=True, choices=[(0, 'dummy')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(max_length=150, choices=[(b'Training', b'Training'), (b'Supervision', b'Supervision'), (b'BCC', b'BCC'), (b'New Distribution', b'New Distribution'), (b'IPTp', b'IPTp'), (b'IRS', b'IRS')]),
        ),
        migrations.AddField(
            model_name='note',
            name='task',
            field=models.ForeignKey(related_name='tasknotes', to='dashboard.Task'),
        ),
    ]
