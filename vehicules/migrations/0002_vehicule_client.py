# Generated by Django 5.1.3 on 2024-12-18 22:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0001_initial'),
        ('vehicules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicule',
            name='client',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='vehicules', to='utilisateurs.client'),
            preserve_default=False,
        ),
    ]
