# Generated by Django 4.2.3 on 2024-10-19 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_unit_current_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='current_week',
            field=models.CharField(default='1', max_length=2, null=True),
        ),
    ]
