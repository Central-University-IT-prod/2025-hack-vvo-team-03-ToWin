# Generated by Django 5.2 on 2025-04-27 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0011_game_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='place',
            field=models.CharField(default=1, max_length=3000),
            preserve_default=False,
        ),
    ]
