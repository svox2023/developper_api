# Generated by Django 5.1.3 on 2024-12-23 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factures', '0002_facture_mecanicien'),
        ('utilisateurs', '0005_client_mecanicien'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='factures', to='utilisateurs.client'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='mecanicien',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factures', to='utilisateurs.mecanicien'),
        ),
    ]
