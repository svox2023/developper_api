# Generated by Django 5.1.3 on 2024-12-23 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendez_vous', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendezvous',
            name='status',
            field=models.CharField(choices=[('en_attente', 'En attente'), ('confirme', 'Confirmé'), ('annule', 'Annulé'), ('termine', 'Terminé')], default='en_attente', max_length=10),
        ),
    ]
