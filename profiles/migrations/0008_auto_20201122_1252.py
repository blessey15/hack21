# Generated by Django 3.0.6 on 2020-11-22 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20201121_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantprofile',
            name='field_of_study',
            field=models.CharField(choices=[('School Student', 'School Student'), ('Bachelor of Science', 'Bachelor of Science'), ('Bachelor of Arts', 'Bachelor of Arts'), ('Bachelor of Technology', 'Bachelor of Technology'), ('Bachelor of Commerce', 'Bachelor of Commerce'), ('Master of Science', 'Master of Science'), ('Master of Arts', 'Master of Arts'), ('Master of Technology', 'Master of Technology'), ('Master of Commerce', 'Master of Commerce'), ('Other', 'Other')], default='BTech', max_length=30, verbose_name='Field of Study'),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Non-Binary', 'Non Binary'), ('N/A', 'Prefer not to say')], max_length=11),
        ),
    ]