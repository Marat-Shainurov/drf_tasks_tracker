# Generated by Django 4.2.4 on 2023-09-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_employee_options_alter_employee_dismissal_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employment_date',
            field=models.DateField(auto_now_add=True, verbose_name='employment_date'),
        ),
    ]
