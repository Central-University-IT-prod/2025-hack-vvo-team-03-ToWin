# Generated by Django 5.2 on 2025-04-25 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='description',
            field=models.CharField(default=1, max_length=2500),
            preserve_default=False,
        ),
    ]
