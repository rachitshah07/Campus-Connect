# Generated by Django 4.1 on 2023-11-05 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_studentresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ce_mark', models.IntegerField()),
                ('assignment_mark', models.IntegerField()),
                ('practical_mark', models.IntegerField()),
                ('lpw_mark', models.IntegerField()),
                ('see_mark', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
            ],
        ),
        migrations.DeleteModel(
            name='StudentResult',
        ),
    ]
