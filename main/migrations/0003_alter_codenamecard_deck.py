# Generated by Django 4.0.5 on 2022-06-26 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_deck_alter_codenamecard_deck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codenamecard',
            name='deck',
            field=models.CharField(default='Unset', max_length=30),
            preserve_default=False,
        ),
    ]