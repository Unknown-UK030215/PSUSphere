# Generated by Django 5.1.6 on 2025-04-03 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentorg', '0005_alter_college_college_name_alter_organization_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
