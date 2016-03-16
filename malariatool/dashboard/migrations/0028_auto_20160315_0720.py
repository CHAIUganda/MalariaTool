# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_auto_20160122_0429'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelDocuments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=120)),
                ('files', models.FileField(upload_to=b'excel_docs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Repository',
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(max_length=150, choices=[(b'not_started', b'Not Started'), (b'ongoing', b'Ongoing'), (b'done', b'Done')]),
        ),
    ]
