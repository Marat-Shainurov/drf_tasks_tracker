# Generated by Django 4.2.4 on 2023-08-31 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_employee_options_alter_employee_dismissal_date_and_more'),
        ('tasks', '0007_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='executor_tasks', to='employees.employee', verbose_name='task_executor'),
        ),
    ]
