# Generated by Django 3.2.4 on 2021-11-02 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Register', '0001_initial'),
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storie',
            name='Owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Register.registermodel'),
        ),
    ]
