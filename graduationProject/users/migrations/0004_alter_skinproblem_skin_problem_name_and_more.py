# Generated by Django 5.1.2 on 2025-03-04 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_skinproblem_skin_problem_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skinproblem',
            name='skin_problem_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='skintype',
            name='skin_type_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
