# Generated manually to add missing fields to existing database

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        # Alter Project slug to be unique
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, db_index=True),
        ),
        
        # Alter Project image path
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(upload_to='projects/'),
        ),
        
        # Add db_index to Project fields
        migrations.AlterField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='ranking',
            field=models.IntegerField(default=7, db_index=True),
        ),
    ]
