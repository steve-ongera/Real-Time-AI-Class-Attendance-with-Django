# Generated by Django 4.2.3 on 2024-10-21 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_alter_unit_current_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='fee_balance',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='year',
            field=models.CharField(max_length=70, null=True),
        ),
    ]