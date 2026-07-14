from django.contrib.auth import get_user_model
from django.db import migrations

def create_superuser(apps, schema_editor):
    User = get_user_model()
    # Replace these with your chosen credentials
    username = 'myadmin'
    password = 'mypassword123'
    email = 'admin@example.com'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)

class Migration(migrations.Migration):
    dependencies = [
        ('tiva', '0007_review'), 
    ]  
    operations = [
        migrations.RunPython(create_superuser),
    ]