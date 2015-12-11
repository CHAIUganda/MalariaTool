# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_task_overview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('description', models.TextField()),
                ('estimated_end_date', models.DateField()),
                ('status', model_utils.fields.StatusField(default=b'not started', max_length=100, no_check_for_status=True, choices=[(b'not started', b'not started'), (b'ongoing', b'ongoing'), (b'done', b'done')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='task',
            name='ip',
            field=models.ForeignKey(related_name='ip_tasks', to='dashboard.IP'),
        ),
        migrations.AddField(
            model_name='task',
            name='sub_tasks',
            field=models.ManyToManyField(to='dashboard.Item'),
        ),
    ]
