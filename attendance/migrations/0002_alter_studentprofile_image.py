# Generated by Django 4.2.3 on 2024-10-16 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='image',
            field=models.ImageField(null=True, upload_to='profile_images/'),
        ),
    ]
