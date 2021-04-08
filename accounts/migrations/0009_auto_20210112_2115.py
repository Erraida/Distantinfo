# Generated by Django 3.1.4 on 2021-01-12 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_auto_20210112_2115'),
        ('accounts', '0008_auto_20210112_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='Group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='editor.group'),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
