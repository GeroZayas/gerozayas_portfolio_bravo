# Generated manually to add missing fields to existing database

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        # Add db_index to ContactProfile
        migrations.AlterField(
            model_name='contactprofile',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        
        # Add db_index to Certificate
        migrations.AlterField(
            model_name='certificate',
            name='date',
            field=models.DateTimeField(blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='is_active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        
        # Alter Certificate image path
        migrations.AlterField(
            model_name='certificate',
            name='certificate_image',
            field=models.ImageField(upload_to='certificates/'),
        ),
    ]
