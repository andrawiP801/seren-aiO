# Generated by Django 5.0.4 on 2024-04-21 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='surname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
