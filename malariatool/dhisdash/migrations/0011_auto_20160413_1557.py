# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhisdash', '0010_datasynctracker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datasynctracker',
            old_name='last_download',
            new_name='last_downloaded',
        ),
        migrations.RenameField(
            model_name='datasynctracker',
            old_name='last_parse',
            new_name='last_parsed',
        ),
    ]
