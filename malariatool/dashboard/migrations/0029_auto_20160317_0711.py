# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_auto_20160315_0720'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExcelDocuments',
            new_name='ExcelDocument',
        ),
    ]
